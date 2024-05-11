
"""
The objects below ensure data integrity and provide a structured way to programmatically interact with the network testing system,
enabling automated test retrieval of test information based on the predefined configurations and rules.

for more information see https://developer.cisco.com/docs/thousandeyes/v6/tests-metadata/#test-metadata
"""
import logging
import re
from enum import Enum
from pprint import pprint

from pydantic import BaseModel, Field, HttpUrl, conint, json
from datetime import datetime
from typing import Optional, List, Dict


class TestType(str, Enum):
    __test__ = False
    agent_to_server = "agent-to-server"
    agent_to_agent = "agent-to-agent"
    bgp = "bgp"
    http_server = "http-server"
    page_load = "page-load"
    web_transactions = "web-transactions"
    api = "api"
    ftp_server = "ftp-server"
    dns_trace = "dns-trace"
    dns_server = "dns-server"
    dns_dnssec = "dns-dnssec"
    sip_server = "sip-server"
    voice = "voice"

class DNSServer(BaseModel):
    serverName: str

class DNSProtocol(str, Enum):
    UDP = 'UDP'
    TCP = 'TCP'

class AlertRule(BaseModel):
    ruleId: int

class ApiLink(BaseModel):
    rel: str
    href: HttpUrl

class Label(BaseModel):
    name: str
    groupId: int
    builtIn: int

class AccountGroup(BaseModel):
    aid: int
    name: str

class Agent(BaseModel):
    agentId: int
    sourceIpAddress: Optional[str] = None

class ProtocolType(str, Enum):
    TCP = 'TCP'
    ICMP = 'ICMP'
    UDP = 'UDP'

class ProbeMode(str, Enum):
    AUTO = 'AUTO'
    SACK = 'SACK'
    SYN = 'SYN'

class Direction(str, Enum):
    TO_TARGET = 'TO_TARGET'
    FROM_TARGET = 'FROM_TARGET'
    BIDIRECTIONAL = 'BIDIRECTIONAL'

class BGPMonitor(BaseModel):
    monitorId: int

class CustomHeaders(BaseModel):
    root: Optional[Dict[str, str]] = {}
    domains: Optional[Dict[str, Dict[str, str]]] = {}
    all: Optional[Dict[str, str]] = {}

class HTTPAuthenticationType(str, Enum):
    NONE = 'NONE'
    BASIC = 'BASIC'
    NTLM = 'NTLM'
    KERBEROS = 'KERBEROS'

class PageLoadingStrategy(str, Enum):
    NORMAL = 'normal'
    EAGER = 'eager'
    NONE = 'none'

class PredefinedVariable(BaseModel):
    key: str
    value: str

class APIRequest(BaseModel):
    method: str
    url: HttpUrl
    headers: Optional[Dict[str, str]]
    body: Optional[str]

class TargetSipCredentials(BaseModel):
    authUser: Optional[str]
    password: Optional[str]
    port: conint(ge=1024, le=65535)
    protocol: Optional[str] = Field('TCP', description="Defaults to TCP")
    sipRegistrar: str
    user: Optional[str]

class AllTestTypes(BaseModel):
    alertsEnabled: Optional[int] = Field(1, description="Enable alerts by setting to 1, disable by setting to 0")
    alertRules: Optional[List[AlertRule]] = Field(None, description="List of alert rule objects")
    apiLinks: List[ApiLink] = Field(..., description="API links related to the test, read-only")
    createdBy: Optional[str] = Field(None, description="Username of the creator, read-only")
    createdDate: Optional[datetime] = Field(None, description="Creation date in UTC, read-only")
    description: Optional[str] = Field('', description="Description of the test, defaults to empty string")
    enabled: Optional[int] = Field(None, description="Enable test by setting to 1, disable by setting to 0")
    groups: Optional[List[Label]] = Field(None, description="Groups the test is associated with")
    liveShare: Optional[int] = Field(None, description="Indicates if a test is shared, read-only")
    modifiedBy: Optional[str] = Field(None, description="Username of the modifier, read-only")
    modifiedDate: Optional[datetime] = Field(None, description="Date of last modification in UTC, read-only")
    savedEvent: Optional[int] = Field(None, description="Indicates if an event is saved, read-only")
    sharedWithAccounts: Optional[List[AccountGroup]] = Field(None, description="Account groups with which the test is shared")
    testId: int = Field(..., description="Unique ID of the test, read-only")
    testName: Optional[str] = Field(None, description="Unique name of the test")
    type: Optional[str] = Field(None, description="Type of test, read-only")

    def __init__(self, **data):
        super().__init__(**data)
        self.redact_sensitive_data()
    def redact_sensitive_data(self):
        print('Redacting sensitive data before sending to out')
        self.createdBy = re.sub(r'\(.*?\)', f'(EMAIL_REDACTED)', self.createdBy)
class BGPTest(AllTestTypes):
    bgpMonitors: Optional[List[BGPMonitor]] = Field(None, description="List of BGP Monitor objects")
    includeCoveredPrefixes: Optional[int] = Field(None, description="Set to 1 to include subprefix queries")
    prefix: str = Field(..., description="Network address with prefix length, e.g., a.b.c.d/e")
    usePublicBgp: Optional[int] = Field(None, description="Set to 1 to use all available Public BGP Monitors")

class AgentToServerTest(AllTestTypes):
    agents: List[Agent]= Field(None)
    bandwidthMeasurements: Optional[int] = Field(None, description="Set to 1 to measure bandwidth")
    bgpMeasurements: Optional[int] = Field(1, description="Enable BGP measurements by setting to 1")
    bgpMonitors: Optional[List[BGPMonitor]]= Field(None)
    continuousMode: Optional[int]= Field(None)
    fixedPacketRate: Optional[int]= Field(None)
    interval: int = Field(..., gt=0, description="Interval in seconds")
    mtuMeasurements: Optional[int]= Field(None)
    numPathTraces: Optional[int] = Field(3, description="Number of path traces")
    pathTraceMode: Optional[str] = Field('classic')
    port: Optional[conint(gt=0, lt=65536)]= Field(None)
    probeMode: Optional[ProbeMode]= Field(None)
    protocol: Optional[ProtocolType] = Field('TCP')
    server: str= Field(None)

class AgentToAgentTest(AllTestTypes):
    agents: List[Agent]= Field(None)
    bgpMeasurements: Optional[int] = Field(1, description="Enable BGP measurements by setting to 1")
    bgpMonitors: Optional[List[BGPMonitor]]= Field(None)
    direction: Optional[Direction] = Field('TO_TARGET', description="Direction of the test")
    dscpId: Optional[int] = Field(0, description="DSCP ID, defaults to 0")
    interval: int = Field(..., gt=0, description="Interval in seconds")
    mss: Optional[conint(gt=29, lt=1401)]= Field(None)
    numPathTraces: Optional[int] = Field(3, description="Number of path traces")
    pathTraceMode: Optional[str] = Field('classic')
    port: Optional[conint(gt=0, lt=65536)] = Field(49153)
    protocol: Optional[ProtocolType] = Field('TCP')
    targetAgentId: Optional[int]= Field(None)
    throughputMeasurements: Optional[int]= Field(None)
    throughputDuration: Optional[conint(gt=4999, lt=30001)]= Field(None)
    throughputRate: Optional[conint(gt=-1, lt=1001)]= Field(None)


class DNSServerTest(AllTestTypes):
    agents: List[Agent]= Field(None)
    dnsServers: List[DNSServer]= Field(None)
    domain: str= Field(None)
    dnsTransportProtocol: Optional[DNSProtocol] = Field('UDP', description="Protocol used for DNS requests")
    interval: int= Field(None)
    bandwidthMeasurements: Optional[int]= Field(None)
    bgpMeasurements: Optional[int] = Field(1, description="Enable BGP measurements by setting to 1")
    bgpMonitors: Optional[List[BGPMonitor]]= Field(None)
    mtuMeasurements: Optional[int]= Field(None)
    networkMeasurements: Optional[int] = Field(1, description="Enable network measurements")
    numPathTraces: Optional[int] = Field(1, description="Number of path traces")
    pathTraceMode: Optional[str] = Field('classic', description="Path trace mode")
    probeMode: Optional[ProbeMode]= Field(None)
    protocol: Optional[str] = Field('TCP', description="Protocol used by dependent Network tests")
    recursiveQueries: Optional[int]= Field(None)

class DNSTraceTest(AllTestTypes):
    agents: List[Agent]
    domain: str
    dnsTransportProtocol: Optional[DNSProtocol] = Field('UDP', description="Protocol used for DNS requests")
    interval: int

class DNSSECTest(AllTestTypes):
    agents: List[Agent]
    domain: str
    interval: int


class HTTPServerTest(AllTestTypes):
    agents: List[Agent]= Field(None)
    authType: Optional[HTTPAuthenticationType] = Field('NONE', description="HTTP Authentication type")
    bandwidthMeasurements: Optional[int]= Field(None)
    bgpMeasurements: Optional[int] = Field(1, description="Enable BGP measurements by default")
    bgpMonitors: Optional[List[BGPMonitor]]= Field(None)
    clientCertificate: Optional[str]= Field(None)
    contentRegex: Optional[str]= Field(None)
    customHeaders: Optional[CustomHeaders]= Field(None)
    desiredStatusCode: Optional[str]= Field(None)
    downloadLimit: Optional[int]= Field(None)
    dnsOverride: Optional[str]= Field(None)
    followRedirects: Optional[int] = Field(1, description="Follow HTTP redirects by default")
    headers: Optional[List[str]]= Field(None)
    httpVersion: Optional[int] = Field(2, description="Prefer HTTP/2 by default")
    httpTargetTime: Optional[int]= Field(None)
    httpTimeLimit: Optional[int] = Field(5, description="HTTP time limit in seconds")
    interval: int= Field(None)
    mtuMeasurements: Optional[int]= Field(None)
    networkMeasurements: Optional[int] = Field(1, description="Enable network measurements by default")
    numPathTraces: Optional[int] = Field(3, description="Default number of path traces")
    password: Optional[str]= Field(None)
    pathTraceMode: Optional[str] = Field('classic', description="Path trace mode")
    postBody: Optional[str]= Field(None)
    probeMode: Optional[str]= Field(None)
    protocol: Optional[str] = Field('TCP', description="Default protocol for network tests")
    sslVersion: Optional[str]= Field(None)
    sslVersionId: Optional[int]= Field(None)
    url: HttpUrl= Field(None)
    useNtlm: Optional[int]= Field(None)
    userAgent: Optional[str]= Field(None)
    username: Optional[str]= Field(None)
    verifyCertificate: Optional[int] = Field(1, description="Verify SSL/TLS certificate by default")
    allowUnsafeLegacyRenegotiation: Optional[int] = Field(1, description="Allow unsafe legacy TLS renegotiation")

class PageLoadTest(AllTestTypes):
    agents: List[Agent]= Field(None)
    authType: Optional[HTTPAuthenticationType] = Field('NONE', description="HTTP Authentication type")
    bandwidthMeasurements: Optional[int]= Field(None)
    bgpMeasurements: Optional[int] = Field(1, description="Enable BGP measurements by default")
    bgpMonitors: Optional[List[BGPMonitor]]= Field(None)
    clientCertificate: Optional[str]= Field(None)
    contentRegex: Optional[str]= Field(None)
    customHeaders: Optional[CustomHeaders]= Field(None)
    httpInterval: Optional[int]= Field(None)
    httpTargetTime: Optional[int]= Field(None)
    httpTimeLimit: Optional[int] = Field(5, description="HTTP time limit in seconds")
    httpVersion: Optional[int] = Field(2, description="Prefer HTTP/2 by default")
    includeHeaders: Optional[int] = Field(1, description="Capture HTTP headers by default")
    interval: int= Field(None)
    mtuMeasurements: Optional[int]= Field(None)
    networkMeasurements: Optional[int] = Field(1, description="Enable network measurements by default")
    numPathTraces: Optional[int] = Field(3, description="Default number of path traces")
    pageLoadTargetTime: Optional[int]= Field(None)
    pageLoadTimeLimit: Optional[int] = Field(10, description="Page load time limit in seconds")
    password: Optional[str]= Field(None)
    pathTraceMode: Optional[str] = Field('classic', description="Path trace mode")
    probeMode: Optional[str]= Field(None)
    protocol: Optional[str] = Field('TCP', description="Default protocol for network tests")
    sslVersion: Optional[str]= Field(None)
    sslVersionId: Optional[int]= Field(None)
    subinterval: Optional[int]= Field(None)
    url: HttpUrl= Field(None)
    useNtlm: Optional[int]= Field(None)
    userAgent: Optional[str]= Field(None)
    username: Optional[str]= Field(None)
    verifyCertificate: Optional[int] = Field(1, description="Verify SSL/TLS certificate by default")
    blockDomains: Optional[str]= Field(None)
    disableScreenshot: Optional[int]= Field(None)
    allowMicAndCamera: Optional[int]= Field(None)
    allowGeolocation: Optional[int]= Field(None)
    browserLanguage: Optional[str] = Field(None)
    pageLoadingStrategy: Optional[str] = Field('normal', description="Page loading strategy")
    allowUnsafeLegacyRenegotiation: Optional[int] = Field(1, description="Allow unsafe TLS renegotiation")


class WebTransactionsTest(AllTestTypes):
    agents: List[Agent]= Field(None)
    authType: Optional[HTTPAuthenticationType] = Field('NONE', description="HTTP Authentication type")
    bandwidthMeasurements: Optional[int] = Field(0, description="Measure bandwidth; defaults to 0")
    contentRegex: Optional[str]= Field(None)
    credentials: Optional[List[int]]= Field(None)
    clientCertificate: Optional[str]= Field(None)
    customHeaders: Optional[CustomHeaders]= Field(None)
    desiredStatusCode: Optional[str]= Field(None)
    followRedirects: Optional[int] = Field(1, description="Follow HTTP redirects by default")
    httpTargetTime: Optional[int]= Field(None)
    httpTimeLimit: Optional[int] = Field(5, description="HTTP time limit in seconds")
    httpVersion: Optional[int] = Field(2, description="Prefer HTTP/2 by default")
    includeHeaders: Optional[int] = Field(1, description="Capture HTTP headers by default")
    interval: int= Field(None)
    mtuMeasurements: Optional[int]= Field(None)
    networkMeasurements: Optional[int] = Field(1, description="Enable network measurements by default")
    numPathTraces: Optional[int] = Field(3, description="Default number of path traces")
    password: Optional[str]= Field(None)
    pathTraceMode: Optional[str] = Field('classic', description="Path trace mode")
    probeMode: Optional[str]= Field(None)
    protocol: Optional[str] = Field('TCP', description="Default protocol for network tests")
    sslVersionId: Optional[int]= Field(None)
    subinterval: Optional[int]= Field(None)
    url: HttpUrl= Field(None)
    useNtlm: Optional[int]= Field(None)
    userAgent: Optional[str]= Field(None)
    username: Optional[str]= Field(None)
    verifyCertificate: Optional[int] = Field(1, description="Verify SSL/TLS certificate by default")
    blockDomains: Optional[str]= Field(None)
    disableScreenshot: Optional[int]= Field(None)
    allowMicAndCamera: Optional[int]= Field(None)
    allowGeolocation: Optional[int]= Field(None)
    browserLanguage: Optional[str]= Field(None)
    pageLoadingStrategy: Optional[PageLoadingStrategy] = Field('normal', description="Page loading strategy")
    allowUnsafeLegacyRenegotiation: Optional[int] = Field(1, description="Allow unsafe TLS renegotiation")
    transactionScript: Optional[str]= Field(None)
    targetTime: Optional[int]= Field(None)
    timeLimit: Optional[int] = Field(30, description="Time limit for the transaction in seconds")

class FTPServerTest(BaseModel):
    agents: List[Agent]= Field(None)
    agents_sourceIpAddress: Optional[str]= Field(None)
    bgpMeasurements: Optional[int] = Field(1, description="Enable BGP measurements by default")
    downloadLimit: Optional[int]= Field(None)
    ftpTargetTime: Optional[int]= Field(None)
    ftpTimeLimit: Optional[int] = Field(10, description="FTP time limit in seconds")
    interval: int= Field(None)
    mtuMeasurements: Optional[int]= Field(None)
    networkMeasurements: Optional[int] = Field(1, description="Enable network measurements by default")
    numPathTraces: Optional[int] = Field(3, description="Default number of path traces")
    password: str= Field(None)
    pathTraceMode: Optional[str] = Field('classic', description="Path trace mode")
    probeMode: Optional[str]= Field(None)
    protocol: Optional[str] = Field('TCP', description="Default protocol for network tests")
    requestType: str= Field(None)
    url: HttpUrl= Field(None)
    useActiveFtp: Optional[int]= Field(None)
    useExplicitFtps: Optional[int]= Field(None)
    username: str= Field(None)



class APITest(BaseModel):
    agents: List[Agent]= Field(None)
    credentials: Optional[List[int]]= Field(None)
    followRedirects: Optional[int] = Field(1, description="Follow redirects by default")
    interval: int= Field(None)
    mtuMeasurements: Optional[int]= Field(None)
    networkMeasurements: Optional[int] = Field(1, description="Enable network measurements by default")
    numPathTraces: Optional[int] = Field(3, description="Default number of path traces")
    pathTraceMode: Optional[str] = Field('classic', description="Path trace mode")
    predefinedVariables: Optional[List[PredefinedVariable]]
    probeMode: Optional[str]= Field(None)
    protocol: Optional[str] = Field('TCP', description="Default protocol for network tests")
    requests: List[APIRequest]= Field(None)
    sslVersionId: Optional[int]= Field(None)
    targetTime: Optional[int]= Field(None)
    timeLimit: Optional[int] = Field(30, description="Time limit for the transaction in seconds")
    url: HttpUrl= Field(None)


class SIPServerTest(BaseModel):
    agents: List[Agent] = Field(None)
    authUser: Optional[str]= Field(None)
    bgpMeasurements: Optional[int] = Field(1, description="Enable BGP measurements by default")
    mtuMeasurements: Optional[int]= Field(None)
    networkMeasurements: Optional[int] = Field(1, description="Enable network measurements by default")
    optionsRegex: Optional[str]= Field(None)
    password: Optional[str]= Field(None)
    pathTraceMode: Optional[str] = Field('classic', description="Path trace mode")
    port: Optional[conint(ge=1024, le=65535)]= Field(None)
    protocol: Optional[str] = Field('TCP', description="Default protocol for SIP tests")
    registerEnabled: Optional[int] = Field(0, description="Disabled by default")
    sipRegistrar: Optional[str]= Field(None)
    sipTargetTime: Optional[int]= Field(None)
    sipTimeLimit: Optional[int] = Field(5, description="Default SIP time limit in seconds")
    targetSipCredentials: TargetSipCredentials
    user: Optional[str]= Field(None)

class RTPStreamTest(BaseModel):
    agents: List[Agent]= Field(None)
    bgpMeasurements: Optional[int] = Field(1, description="Enable BGP measurements by default")
    codecId: Optional[int] = Field(0, description="Default codec ID")
    dscpId: Optional[int] = Field(46, description="Default DSCP ID for RTP")
    duration: Optional[int] = Field(5, description="Duration of the test in seconds")
    interval: int= Field(None)
    jitterBuffer: Optional[int] = Field(40, description="De-jitter buffer size in milliseconds")
    numPathTraces: Optional[int] = Field(3, description="Default number of path traces")
    port: Optional[conint(ge=1024, le=65535)] = Field(49152, description="Default port for RTP")
    targetAgentId: int= Field(None)


def validate_test_data(data: dict):
    if 'type' not in data:
        logging.error("Test type is required but not provided.")
        raise ValueError("Test type is required but not provided.")

    try:
        test_type = TestType(data['type'])
    except ValueError as e:
        logging.error(f"Invalid test type provided: {data.get('type')}")
        raise ValueError(f"Invalid test type provided: {data.get('type')}") from e

    test_class_map = {
        TestType.agent_to_server: AgentToServerTest,
        TestType.agent_to_agent: AgentToAgentTest,
        TestType.bgp: BGPTest,
        TestType.http_server: HTTPServerTest,
        TestType.page_load: PageLoadTest,
        TestType.web_transactions: WebTransactionsTest,
        TestType.api: APITest,
        TestType.ftp_server: FTPServerTest,
        TestType.dns_trace: DNSTraceTest,
        TestType.dns_server: DNSServerTest,
        TestType.dns_dnssec: DNSSECTest,
        TestType.sip_server: SIPServerTest,
        TestType.voice: RTPStreamTest,
    }

    test_class = test_class_map.get(test_type)
    if not test_class:
        logging.error(f"Test class not found for the type: {test_type}")
        raise ValueError(f"Test class not found for the type: {test_type}")

    logging.info(f"Creating test object for type: {test_type}")
    return test_class(**data).json()