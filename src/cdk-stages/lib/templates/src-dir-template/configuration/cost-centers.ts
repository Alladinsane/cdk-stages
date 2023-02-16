const analytics = [
    'AWS::Athena::DataCatalog',
    'AWS::Athena::WorkGroup',
    'AWS::KinesisAnalyticsV2::Application'
];

const database = [
    'AWS::DocDB::DBCluster',
    'AWS::DocDB::DBClusterParameterGroup',
    'AWS::DocDB::DBInstance',
    'AWS::DocDB::DBSubnetGroup',
    'AWS::DynamoDB::Table',
    'AWS::RDS::DBCluster',
    'AWS::RDS::DBClusterParameterGroup',
    'AWS::RDS::DBInstance',
    'AWS::RDS::DBParameterGroup',
    'AWS::RDS::DBProxy',
    'AWS::RDS::DBProxyEndpoint',
    'AWS::RDS::DBSecurityGroup',
    'AWS::RDS::DBSubnetGroup',
    'AWS::RDS::OptionGroup',
    'AWS::Redshift::Cluster',
    'AWS::Redshift::ClusterParameterGroup',
    'AWS::Redshift::ClusterSecurityGroup',
    'AWS::Redshift::ClusterSubnetGroup',
    'AWS::Redshift::EventSubscription'
];

const delivery = [
    'AWS::CodeArtifact::Domain',
    'AWS::CodeArtifact::Repository',
    'AWS::CodeBuild::Project',
    'AWS::CodeBuild::ReportGroup',
    'AWS::CodePipeline::CustomActionType',
    'AWS::CodePipeline::Pipeline'
];

const dev = [
    'AWS::CodeGuruProfiler::ProfilingGroup',
    'AWS::CodeGuruReviewer::RepositoryAssociation',
    'AWS::Lambda::Function',
    'AWS::XRay::Group',
    'AWS::XRay::SamplingRule'
];

const disasterRecovery = [
    'AWS::Backup::BackupPlan',
    'AWS::Backup::BackupVault',
    'AWS::Backup::Framework',
    'AWS::Backup::ReportPlan'
];

const infrastructure = [
    'AWS::CertificateManager::Certificate',
    'AWS::EC2::CapacityReservation',
    'AWS::EC2::CapacityReservationFleet',
    'AWS::EC2::DHCPOptions',
    'AWS::EC2::EC2Fleet',
    'AWS::ImageBuilder::Component',
    'AWS::ImageBuilder::ContainerRecipe',
    'AWS::ImageBuilder::DistributionConfiguration',
    'AWS::ImageBuilder::Image',
    'AWS::ImageBuilder::ImagePipeline',
    'AWS::ImageBuilder::ImageRecipe',
    'AWS::ImageBuilder::InfrastructureConfiguration',
    'AWS::EC2::Instance',
    'AWS::EC2::LaunchTemplate',
    'AWS::EC2::NetworkInterface',
    'AWS::EC2::Volume'
];

const marketing = [
    'AWS::SES::ContactList',
    'AWS::Pinpoint::Campaign',
    'AWS::Pinpoint::EmailTemplate',
    'AWS::Pinpoint::InAppTemplate',
    'AWS::Pinpoint::PushTemplate',
    'AWS::Pinpoint::Segment',
    'AWS::Pinpoint::SmsTemplate',
    'AWS::PinpointEmail::ConfigurationSet',
    'AWS::PinpointEmail::DedicatedIpPool',
    'AWS::PinpointEmail::Identity'
];

const monitoring = [
    'AWS::ApplicationInsights::Application',
    'AWS::CloudWatch::InsightRule',
    'AWS::CloudWatch::MetricStream',
    'AWS::Logs::LogGroup',
    'AWS::Route53::HealthCheck',
    'AWS::Synthetics::Canary'
];

const network = [
    'AWS::EC2::CarrierGateway',
    'AWS::EC2::ClientVpnEndpoint',
    'AWS::EC2::CustomerGateway',
    'AWS::EC2::EIP',
    'AWS::EC2::FlowLog',
    'AWS::EC2::InternetGateway',
    'AWS::EC2::IPAM',
    'AWS::EC2::IPAMPool',
    'AWS::EC2::IPAMScope',
    'AWS::EC2::LocalGatewayRouteTableVPCAssociation',
    'AWS::EC2::NatGateway',
    'AWS::EC2::NetworkAcl',
    'AWS::EC2::NetworkInsightsAccessScope',
    'AWS::EC2::NetworkInsightsAccessScopeAnalysis',
    'AWS::EC2::NetworkInsightsAnalysis',
    'AWS::EC2::NetworkInsightsPath',
    'AWS::EC2::PrefixList',
    'AWS::EC2::RouteTable',
    'AWS::EC2::SecurityGroup',
    'AWS::EC2::Subnet',
    'AWS::EC2::TrafficMirrorFilter',
    'AWS::EC2::TrafficMirrorSession',
    'AWS::EC2::TrafficMirrorTarget',
    'AWS::EC2::TransitGateway',
    'AWS::EC2::TransitGatewayAttachment',
    'AWS::EC2::TransitGatewayConnect',
    'AWS::EC2::TransitGatewayMulticastDomain',
    'AWS::EC2::TransitGatewayPeeringAttachment',
    'AWS::EC2::TransitGatewayRouteTable',
    'AWS::EC2::TransitGatewayVpcAttachment',
    'AWS::EC2::VPC',
    'AWS::EC2::VPCPeeringConnection',
    'AWS::EC2::VPNConnection',
    'AWS::EC2::VPNGateway'
];

const operations = [
    'AWS::Events::EventBus',
    'AWS::EventSchemas::Discoverer',
    'AWS::EventSchemas::Registry',
    'AWS::EventSchemas::Schema',
    'AWS::Route53::HostedZone',
    'AWS::Route53Resolver::ResolverEndpoint',
    'AWS::Route53Resolver::ResolverRule',
    'AWS::Kinesis::Stream',
    'AWS::KinesisFirehose::DeliveryStream',
    'AWS::RAM::ResourceShare',
    'AWS::SNS::Topic',
    'AWS::SQS::Queue',
    'AWS::SSM::Document',
    'AWS::SSM::MaintenanceWindow',
    'AWS::SSM::Parameter'
];

const security = [
    'AWS::AccessAnalyzer::Analyzer',
    'AWS::Config::AggregationAuthorization',
    'AWS::Config::ConfigurationAggregator',
    'AWS::Config::StoredQuery',
    'AWS::IAM::OIDCProvider',
    'AWS::IAM::Role',
    'AWS::IAM::SAMLProvider',
    'AWS::IAM::ServerCertificate',
    'AWS::IAM::User',
    'AWS::IAM::VirtualMFADevice',
    'AWS::KMS::Key',
    'AWS::KMS::ReplicaKey',
    'AWS::NetworkFirewall::Firewall',
    'AWS::NetworkFirewall::FirewallPolicy',
    'AWS::NetworkFirewall::LoggingConfiguration',
    'AWS::NetworkFirewall::RuleGroup',
    'AWS::Route53Resolver::FirewallDomainList',
    'AWS::Route53Resolver::FirewallRuleGroup',
    'AWS::Route53Resolver::FirewallRuleGroupAssociation',
    'AWS::SSM::PatchBaseline',
    'AWS::WAFv2::IPSet',
    'AWS::WAFv2::RegexPatternSet',
    'AWS::WAFv2::RuleGroup',
    'AWS::WAFv2::WebACL'
];

//const uncategorized = [...analytics, ...database, ...delivery, ...dev, ...disasterRecovery, ...infrastructure, ...marketing, ...monitoring, ...network, ...operations, ...security];

export { analytics, database, delivery, dev, disasterRecovery, infrastructure, marketing, monitoring, network, operations, security }