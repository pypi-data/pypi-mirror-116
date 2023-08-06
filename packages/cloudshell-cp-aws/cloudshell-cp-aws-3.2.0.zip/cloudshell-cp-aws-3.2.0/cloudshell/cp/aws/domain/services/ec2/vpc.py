import traceback
from typing import TYPE_CHECKING, List, Optional

from retrying import retry

from cloudshell.cp.aws.common import retry_helper
from cloudshell.cp.aws.domain.conncetivity.operations.traffic_mirror_cleaner import (
    TrafficMirrorCleaner,
)
from cloudshell.cp.aws.models.aws_ec2_cloud_provider_resource_model import VpcMode

if TYPE_CHECKING:
    from logging import Logger

    from mypy_boto3_ec2 import EC2ServiceResource
    from mypy_boto3_ec2.service_resource import RouteTable, Subnet, Vpc

    from cloudshell.cp.aws.models.aws_ec2_cloud_provider_resource_model import (
        AWSEc2CloudProviderResourceModel,
    )
    from cloudshell.cp.aws.models.reservation_model import ReservationModel


class VPCService:
    VPC_RESERVATION = "VPC Reservation: {0}"
    SUBNET_RESERVATION = "{0} Reservation: {1}"
    MAIN_ROUTE_TABLE_RESERVATION = "Main RoutingTable Reservation: {0}"
    PRIVATE_ROUTE_TABLE_RESERVATION = "Private RoutingTable Reservation: {0}"
    # RT for public subnets in Shared VPC
    PUBLIC_ROUTE_TABLE_RESERVATION = "Public RoutingTable Reservation: {}"
    PEERING_CONNECTION = "Peering connection for {0} with management vpc"

    def __init__(
        self,
        tag_service,
        subnet_service,
        instance_service,
        vpc_waiter,
        vpc_peering_waiter,
        sg_service,
        route_table_service,
        traffic_mirror_service,
    ):
        """# noqa
        :param tag_service: Tag Service
        :type tag_service: cloudshell.cp.aws.domain.services.ec2.tags.TagService
        :param subnet_service: Subnet Service
        :type subnet_service: cloudshell.cp.aws.domain.services.ec2.subnet.SubnetService
        :param instance_service: Instance Service
        :type instance_service: cloudshell.cp.aws.domain.services.ec2.instance.InstanceService
        :param vpc_waiter: Vpc Peering Connection Waiter
        :type vpc_waiter: cloudshell.cp.aws.domain.services.waiters.vpc.VPCWaiter
        :param vpc_peering_waiter: Vpc Peering Connection Waiter
        :type vpc_peering_waiter: cloudshell.cp.aws.domain.services.waiters.vpc_peering.VpcPeeringConnectionWaiter
        :param sg_service: Security Group Service
        :type sg_service: cloudshell.cp.aws.domain.services.ec2.security_group.SecurityGroupService
        :param route_table_service:
        :type route_table_service: cloudshell.cp.aws.domain.services.ec2.route_table.RouteTablesService
        """
        self.tag_service = tag_service
        self.subnet_service = subnet_service
        self.instance_service = instance_service
        self.vpc_waiter = vpc_waiter
        self.vpc_peering_waiter = vpc_peering_waiter
        self.sg_service = sg_service
        self.route_table_service = route_table_service
        self.traffic_mirror_service = traffic_mirror_service

    def create_vpc_for_reservation(self, ec2_session, reservation, cidr):
        """# noqa
        Will create a vpc for reservation and will save it in a folder in the s3 bucket
        :param ec2_session: Ec2 Session
        :param reservation: reservation model
        :type reservation: cloudshell.cp.aws.models.reservation_model.ReservationModel
        :param cidr: The CIDR block
        :type cidr: str
        :return: vpc
        """
        vpc = ec2_session.create_vpc(CidrBlock=cidr)

        self.vpc_waiter.wait(vpc=vpc, state=self.vpc_waiter.AVAILABLE)

        vpc_name = self.VPC_RESERVATION.format(reservation.reservation_id)
        self._set_tags(vpc_name=vpc_name, reservation=reservation, vpc=vpc)

        return vpc

    def get_or_create_subnet_for_vpc(
        self, reservation, cidr, alias, vpc, ec2_client, aws_ec2_datamodel, logger
    ):

        logger.info(f"Check if subnet (cidr={cidr}) already exists")
        subnet = self.subnet_service.get_first_or_none_subnet_from_vpc(
            vpc=vpc, cidr=cidr
        )
        if subnet:
            return subnet

        subnet_name = self.SUBNET_RESERVATION.format(alias, reservation.reservation_id)
        availability_zone = self.get_or_pick_availability_zone(
            ec2_client, vpc, aws_ec2_datamodel
        )
        logger.info(
            f"Create subnet (alias: {alias}, cidr: {cidr}, availability-zone: "
            f"{availability_zone})"
        )
        return self.subnet_service.create_subnet_for_vpc(
            vpc=vpc,
            cidr=cidr,
            subnet_name=subnet_name,
            availability_zone=availability_zone,
            reservation=reservation,
        )

    def get_or_throw_private_route_table(
        self, vpc: "Vpc", reservation_id: str
    ) -> "RouteTable":
        route_table_name = self.PRIVATE_ROUTE_TABLE_RESERVATION.format(reservation_id)
        route_table = self.route_table_service.get_route_table(vpc, route_table_name)
        if not route_table:
            raise ValueError("Routing table for non-public subnet was not found")
        return route_table

    def get_or_create_private_route_table(
        self, vpc: "Vpc", reservation: "ReservationModel"
    ) -> "RouteTable":
        route_table_name = self.PRIVATE_ROUTE_TABLE_RESERVATION.format(
            reservation.reservation_id
        )
        route_table = self.route_table_service.get_route_table(vpc, route_table_name)
        if not route_table:
            route_table = self.route_table_service.create_route_table(
                vpc, reservation, route_table_name
            )
        return route_table

    def get_or_create_public_route_table(
        self,
        vpc: "Vpc",
        reservation: "ReservationModel",
    ) -> "RouteTable":
        name = self.PUBLIC_ROUTE_TABLE_RESERVATION.format(reservation.reservation_id)
        route_table = self.route_table_service.get_route_table(vpc, name)
        if not route_table:
            route_table = self.route_table_service.create_route_table(
                vpc, reservation, name
            )
        return route_table

    def get_or_throw_public_route_table(
        self,
        vpc: "Vpc",
        reservation_id: str,
    ) -> "RouteTable":
        name = self.PUBLIC_ROUTE_TABLE_RESERVATION.format(reservation_id)
        route_table = self.route_table_service.get_route_table(vpc, name)
        if not route_table:
            raise ValueError("Routing table for public subnet was not found")
        return route_table

    def find_vpc_for_reservation(
        self, ec2_session: "EC2ServiceResource", reservation_id: str
    ) -> Optional["Vpc"]:
        filters = [
            {
                "Name": "tag:Name",
                "Values": [self.VPC_RESERVATION.format(reservation_id)],
            }
        ]

        vpcs = list(ec2_session.vpcs.filter(Filters=filters))

        if not vpcs:
            return None

        if len(vpcs) > 1:
            raise ValueError("Too many vpcs for the reservation")

        return vpcs[0]

    def get_vpc(
        self,
        ec2_session: "EC2ServiceResource",
        reservation_id: str,
        aws_ec2_datamodel: "AWSEc2CloudProviderResourceModel",
    ) -> Optional["Vpc"]:
        if aws_ec2_datamodel.vpc_mode is VpcMode.SHARED:
            return self.get_vpc_by_id(ec2_session, aws_ec2_datamodel.vpc_id)
        else:
            return self.find_vpc_for_reservation(ec2_session, reservation_id)

    @staticmethod
    def get_vpc_by_id(ec2_session: "EC2ServiceResource", vpc_id: str) -> "Vpc":
        return ec2_session.Vpc(vpc_id)

    def peer_vpcs(
        self,
        ec2_session: "EC2ServiceResource",
        vpc_id1: str,
        vpc_id2: str,
        reservation_model: "ReservationModel",
        logger: "Logger",
    ) -> str:
        """Will create a peering request between 2 vpc's and approve it."""
        # create peering connection
        logger.info(f"Creating VPC Peering between {vpc_id1} to {vpc_id2} ")
        vpc_peer_connection = ec2_session.create_vpc_peering_connection(
            VpcId=vpc_id1, PeerVpcId=vpc_id2
        )
        logger.info(
            f"VPC Peering created {vpc_peer_connection.id}, "
            f"State : {vpc_peer_connection.status['Code']}"
        )

        # wait until pending acceptance
        logger.info("Waiting until VPC peering state will be pending-acceptance ")
        self.vpc_peering_waiter.wait(
            vpc_peer_connection, self.vpc_peering_waiter.PENDING_ACCEPTANCE
        )
        logger.info(f"VPC peering state {vpc_peer_connection.status['Code']}")

        # accept peering request (will try 3 times)
        self.accept_vpc_peering(vpc_peer_connection, logger)

        # wait until active
        logger.info(
            f"Waiting until VPC peering state will be {self.vpc_peering_waiter.ACTIVE}"
        )
        self.vpc_peering_waiter.wait(
            vpc_peer_connection, self.vpc_peering_waiter.ACTIVE
        )
        logger.info(f"VPC peering state {vpc_peer_connection.status['Code']}")

        # set tags on peering connection
        tags = self.tag_service.get_default_tags(
            self._get_peering_connection_name(reservation_model), reservation_model
        )
        retry_helper.do_with_retry(
            lambda: ec2_session.create_tags(
                Resources=[vpc_peer_connection.id], Tags=tags
            )
        )

        return vpc_peer_connection.id

    @retry(stop_max_attempt_number=30, wait_fixed=1000)
    def accept_vpc_peering(self, vpc_peer_connection, logger):
        logger.info(f"Accepting VPC Peering {vpc_peer_connection.id}")
        vpc_peer_connection.accept()
        logger.info(f"VPC Peering {vpc_peer_connection.id} accepted")

    def get_peering_connection_by_reservation_id(self, ec2_session, reservation_id):
        """# noqa
        :param ec2_session:
        :param str reservation_id:
        :return:
        """
        return list(
            ec2_session.vpc_peering_connections.filter(
                Filters=[{"Name": "tag:ReservationId", "Values": [reservation_id]}]
            )
        )

    def _get_peering_connection_name(self, reservation_model):
        return self.PEERING_CONNECTION.format(reservation_model.reservation_id)

    def _set_tags(self, vpc_name, reservation, vpc):
        tags = self.tag_service.get_default_tags(vpc_name, reservation)
        self.tag_service.set_ec2_resource_tags(vpc, tags)

    def remove_all_internet_gateways(self, vpc):
        """Removes all internet gateways from a VPC.

        :param vpc: EC2 VPC instance
        """
        internet_gateways = self.get_all_internet_gateways(vpc)
        for ig in internet_gateways:
            ig.detach_from_vpc(VpcId=vpc.id)
            ig.delete()

    def get_all_internet_gateways(self, vpc):
        """Get.

        :param vpc:
        :return:
        :rtype: list
        """
        return list(vpc.internet_gateways.all())

    def create_and_attach_internet_gateway(
        self,
        ec2_session: "EC2ServiceResource",
        vpc: "Vpc",
        reservation: "ReservationModel",
    ) -> str:
        internet_gateway = ec2_session.create_internet_gateway()
        tags = self.tag_service.get_default_tags(
            f"IGW {reservation.reservation_id}", reservation
        )
        self.tag_service.set_ec2_resource_tags(resource=internet_gateway, tags=tags)
        vpc.attach_internet_gateway(InternetGatewayId=internet_gateway.id)
        return internet_gateway.id

    def remove_all_peering(self, vpc):
        """Remove all peering to that VPC.

        :param vpc: EC2 VPC instance
        :return:
        """
        peerings = list(vpc.accepted_vpc_peering_connections.all())
        for peer in peerings:
            if peer.status["Code"] != "failed":
                peer.delete()
        return True

    def remove_all_security_groups(self, vpc: "Vpc"):
        security_groups = list(vpc.security_groups.all())
        for sg in self.sg_service.sort_sg_list(security_groups):
            self.sg_service.delete_security_group(sg)

    def remove_all_subnets(self, vpc):
        """Will remove all attached subnets to that vpc.

        :param vpc: EC2 VPC instance
        :return:
        """
        subnets = list(vpc.subnets.all())
        for subnet in subnets:
            self.subnet_service.delete_subnet(subnet)
        return True

    def delete_all_instances(self, vpc):
        instances = list(vpc.instances.all())
        self.instance_service.terminate_instances(instances)
        return True

    def delete_vpc(self, vpc):
        """Will delete the vpc instance.

        :param vpc: VPC instance
        :return:
        """
        vpc.delete()
        return True

    def get_vpc_cidr(self, ec2_session, vpc_id):
        vpc = ec2_session.Vpc(vpc_id)
        return vpc.cidr_block

    def modify_vpc_attribute(self, ec2_client, vpc_id, enable_dns_hostnames):
        """Enables VPC Attribute.

        :param ec2_client:
        :param vpc_id:
        :param enable_dns_hostnames:
        :return:
        """
        return ec2_client.modify_vpc_attribute(
            EnableDnsHostnames={"Value": enable_dns_hostnames}, VpcId=vpc_id
        )

    def get_or_pick_availability_zone(self, ec2_client, vpc, aws_ec2_datamodel):
        """Return a list of AvailabilityZones, available.

        :param ec2_client:
        :param vpc:
        :param AWSEc2CloudProviderResourceModel aws_ec2_datamodel:
        :return: str
        """
        # pick one of the vpc's subnets
        used_subnet = self.subnet_service.get_first_or_none_subnet_from_vpc(vpc)
        if used_subnet:
            return used_subnet.availability_zone

        # get one zone from the cloud-provider region's AvailabilityZones
        zones = ec2_client.describe_availability_zones(
            Filters=[
                {"Name": "state", "Values": ["available"]},
                {"Name": "region-name", "Values": [aws_ec2_datamodel.region]},
            ]
        )
        if zones and zones.get("AvailabilityZones"):
            return zones["AvailabilityZones"][0]["ZoneName"]

        # edge case - not supposed to happen
        raise ValueError("No AvailabilityZone is available for this vpc")

    def remove_custom_route_tables(self, ec2_session, vpc):
        """Will remove all the routing tables of that vpc.

        :param vpc: EC2 VPC instance
        :return:
        """
        custom_tables = self.route_table_service.get_custom_route_tables(
            ec2_session, vpc.id
        )
        for table in custom_tables:
            self.route_table_service.delete_table(table)
        return True

    def set_main_route_table_tags(self, main_route_table, reservation):
        table_name = self.MAIN_ROUTE_TABLE_RESERVATION.format(
            reservation.reservation_id
        )
        tags = self.tag_service.get_default_tags(table_name, reservation)
        self.tag_service.set_ec2_resource_tags(main_route_table, tags)

    def set_public_route_table_tags(
        self, public_rt: "RouteTable", reservation: "ReservationModel"
    ):
        name = self.PUBLIC_ROUTE_TABLE_RESERVATION.format(reservation.reservation_id)
        tags = self.tag_service.get_default_tags(name, reservation)
        self.tag_service.set_ec2_resource_tags(public_rt, tags)

    def get_active_vpcs_count(self, ec2_client, logger):
        result = None

        try:
            result = len(ec2_client.describe_vpcs()["Vpcs"])

        except Exception:
            logger.error(f"Error querying VPCs count. Error: {traceback.format_exc()}")

        return result

    def delete_traffic_mirror_elements(
        self, ec2_client, traffic_mirror_service, reservation_id, logger
    ):
        """Delete.

        :param logging.Logger logger:
        :param cloudshell.cp.aws.domain.services.ec2.mirroring.TrafficMirrorService traffic_mirror_service:  # noqa: E501
        :param uuid.uuid4 reservation_id:
        :return:
        """
        session_ids = traffic_mirror_service.find_mirror_session_ids_by_reservation_id(
            ec2_client, reservation_id
        )
        filter_ids = (
            traffic_mirror_service.find_traffic_mirror_filter_ids_by_reservation_id(
                ec2_client, reservation_id
            )
        )
        target_ids = (
            traffic_mirror_service.find_traffic_mirror_targets_by_reservation_id(
                ec2_client, reservation_id
            )
        )
        try:
            TrafficMirrorCleaner.cleanup(
                logger, ec2_client, session_ids, filter_ids, target_ids
            )
        except Exception:
            logger.exception(
                "Failed to cleanup traffic mirror elements during reservation cleanup"
            )

    @staticmethod
    def find_subnets_by_reservation_id(
        vpc: "Vpc", reservation_id: str
    ) -> List["Subnet"]:
        return list(
            vpc.subnets.filter(
                Filters=[{"Name": "tag:ReservationId", "Values": [reservation_id]}]
            )
        )
