import csv
import datetime
import hashlib
import os

from dpkt import ethernet, ip, ip6
from dpkt.utils import inet_to_str
from .pcap_extractor.mail import Mail
from .pcap_extractor.TCPFlow import TCPFlow
from .pcap_extractor.DNSExtractor import DNSItem
from .pcap_extractor.HTTPParser import HttpData
from abc import ABCMeta, abstractmethod


class DictSerializable(object):
    """
    可序列化为字典的类的基类 => 继承本抽象类的类拥有序列化成字典的能力
    """
    __metaclass__ = ABCMeta  # 指定这是一个抽象类

    @abstractmethod
    def toDict(self) -> dict:
        pass


class TCPMixin(DictSerializable):
    """
    TCP记录，所有继承本类的记录都拥有记录TCP属性的功能
    """

    def __init__(self):
        self.srcIP = ""
        self.srcPort = 0
        self.dstIP = ""
        self.dstPort = 0
        self.startTime = 0
        self.endTime = 0

    def setTCP(self, tcpFlow: TCPFlow):
        self.srcIP = tcpFlow.srcIP
        self.srcPort = tcpFlow.srcPort
        self.dstIP = tcpFlow.dstIP
        self.dstPort = tcpFlow.dstPort
        self.startTime = tcpFlow.startTime
        self.endTime = tcpFlow.lastTime

    def toDict(self) -> dict:
        return {
            "srcIP": self.srcIP,
            "srcPort": self.srcPort,
            "dstIP": self.dstIP,
            "dstPort": self.dstPort
        }


class IPMixin(DictSerializable):
    """
    IP记录，所有继承本类的记录都拥有记录IP地址的功能
    """

    def __init__(self):
        self.srcIP = ""
        self.dstIP = ""

    def setIP(self, ethPacket: ethernet.Ethernet):
        ipPacket = ethPacket.data
        self.srcIP = inet_to_str(ipPacket.src)
        self.dstIP = inet_to_str(ipPacket.dst)

    def toDict(self) -> dict:
        return {
            "srcIP": self.srcIP,
            "dstIP": self.dstIP
        }


class RecordBase(DictSerializable):
    """
    所有报告记录的基类
    """

    __metaclass__ = ABCMeta  # 指定这是一个抽象类

    def __init__(self):
        # 记录观察到的那些值是危险的
        self.observables = []

    def setObservables(self, observables: [dict]):
        self.observables = observables

    def toDict(self) -> dict:
        return {
            "observables": self.observables
        }


class FileHash(DictSerializable):
    """
    表示文件Hash值
    """

    def __init__(self, data: bytes = None):
        if data:
            self.md5 = hashlib.md5(data).hexdigest()
            self.sha1 = hashlib.sha1(data).hexdigest()
            self.sha256 = hashlib.sha256(data).hexdigest()
        else:
            self.md5 = ""
            self.sha1 = ""
            self.sha256 = ""

    def toDict(self) -> dict:
        return {
            "md5": self.md5,
            "sha1": self.sha1,
            "sha256": self.sha256
        }


class FileItem(DictSerializable):
    """
    文件条目
    """

    def __init__(self, fileData: bytes, filename: str = "", fileType: str = ""):
        self.filename = filename
        self.fileType = fileType
        self.fileHash = FileHash(fileData)

    def toDict(self) -> dict:
        return {
            "filename": self.filename,
            "fileType": self.fileType,
            "fileHash": self.fileHash.toDict()
        }


class EmailRecord(RecordBase, TCPMixin):
    """
    Email记录
    """

    def __init__(self):
        super().__init__()
        self.plain = ""  # 消息内容
        self.html = ""  # html格式的内容
        self.From = ""  # 发件人地址
        self.To = ""  # 收件人地址
        self.Cc = ""  # 抄送地址
        # self.Date = ""  # 日期和时间
        self.Subject = ""  # 主题
        self.MessageID = ""  # 消息ID
        self.files = []

    def initByMailAndObservable(self, mail: Mail):
        self.plain = mail.plain
        if isinstance(self.plain, bytes):
            self.plain = self.plain.decode()
        self.html = mail.html
        self.From = mail.From
        self.To = mail.To
        self.Cc = mail.Cc
        # self.Date = mail.Date
        self.Subject = mail.Subject
        self.MessageID = mail.MessageID
        for mailFile in mail.files:
            self.files.append(FileItem(mailFile.fileData, mailFile.fileName, mailFile.fileType))

    def toDict(self) -> dict:
        filesDict = []
        for file in self.files:
            filesDict.append(file.toDict())
        return {
            "plain": self.plain,
            "html": self.html,
            "from": self.From,
            "to": self.To,
            "cc": self.Cc,
            # "date": self.Date,
            "subject": self.Subject,
            "messageId": self.MessageID,
            "files": filesDict,
            **RecordBase.toDict(self),
            **TCPMixin.toDict(self)
        }


class DNSRecord(RecordBase, IPMixin):
    """
    DNS解析记录
    """

    def __init__(self):
        super().__init__()
        self.domain = ""
        self.domain_type = ""
        self.value = ""
        self.timestamp = 0

    def initByDNSItem(self, item: DNSItem):
        self.domain = item.domain
        self.domain_type = item.domain_type
        self.value = item.value
        self.timestamp = item.timestamp
        self.setIP(item.ethPacket)

    def toDict(self) -> dict:
        return {
            "domain": self.domain,
            "domain_type": self.domain_type,
            "value": self.value,
            "timestamp": self.timestamp,
            **RecordBase.toDict(self),
            **IPMixin.toDict(self)
        }


class HTTPRecord(RecordBase, TCPMixin):
    """
    HTTP记录
    """

    class HttpRequest(DictSerializable):
        """
        HTTP请求记录
        """

        def __init__(self, httpData: HttpData):
            self.uri = httpData.request.uri
            self.method = httpData.request.method
            self.headers = httpData.request.headers
            self.version = httpData.request.version
            self.domain = httpData.getDomain()
            self.url = httpData.getUrl()

        def toDict(self) -> dict:
            return {
                "uri": self.uri,
                "method": self.method,
                "headers": self.headers,
                "version": self.version,
                "domain": self.domain,
                "url": self.url
            }

    class HttpResponse(DictSerializable):
        """
        HTTP响应记录
        """

        def __init__(self, httpData: HttpData):
            self.status = httpData.response.status
            self.reason = httpData.response.reason
            self.body = httpData.response.body
            self.headers = httpData.response.headers
            self.version = httpData.response.version

        def toDict(self) -> dict:
            return {
                "status": self.status,
                "reason": self.reason,
                # "body": self.body,
                "headers": self.headers,
                "version": self.version
            }

    def __init__(self, httpData: HttpData):
        super().__init__()
        self.request = HTTPRecord.HttpRequest(httpData)
        self.response = HTTPRecord.HttpResponse(httpData)

    def toDict(self) -> dict:
        return {
            "request": self.request.toDict(),
            "response": self.response.toDict(),
            **RecordBase.toDict(self),
            **TCPMixin.toDict(self)
        }


class FileHashRecord(RecordBase, TCPMixin):
    """
    FTP 记录
    """

    def __init__(self, data: bytes = None):
        super().__init__()
        self.fileHash = None
        self.filename = ""
        if data:
            self.fileHash = FileHash(data)

    def getValue(self):
        return f"{self.fileHash.md5}-{self.fileHash.sha1}-{self.fileHash.sha256}"

    def toDict(self) -> dict:
        return {
            "fileHash": self.fileHash.toDict(),
            **RecordBase.toDict(self),
            **TCPMixin.toDict(self)
        }


class Report(DictSerializable):
    """
    对比报告
    """

    def toDict(self) -> dict:
        emailRecordsDict = []
        fileHashRecordsDict = []
        httpRecordsDict = []
        domainRecordsDict = []
        for emailRecord in self.emailRecords:
            emailRecordsDict.append(emailRecord.toDict())
        for fileHashRecord in self.fileHashRecords:
            fileHashRecordsDict.append(fileHashRecord.toDict())
        for httpRecord in self.httpRecords:
            httpRecordsDict.append(httpRecord.toDict())
        for domainRecord in self.domainRecords:
            domainRecordsDict.append(domainRecord.toDict())
        return {
            "totalPacket": self.totalPacket,
            "totalIPAddress": self.totalIPAddress,
            "totalIPv6Address": self.totalIPv6Address,
            "totalIPPacket": self.totalIPPacket,
            "totalIPv6Packet": self.totalIPv6Packet,
            "duration": self.duration,
            "totalTCPFlowNum": self.totalTCPFlowNum,
            "totalHTTPNum": self.totalHTTPNum,
            "totalFTPNum": self.totalFTPNum,
            "totalEmailNum": self.totalEmailNum,
            "totalFileNum": self.totalFileNum,
            "totalDomainNum": self.totalDomainNum,
            "totalMatchIpAddress": self.totalMatchIpAddress,
            "totalMatchIpv6Address": self.totalMatchIpv6Address,
            "totalMatchEmailNum": self.totalMatchEmailNum,
            "totalMatchDomain": self.totalMatchDomain,
            "totalMatchFileHash": self.totalMatchFileHash,
            "totalMatchUri": self.totalMatchUri,

            "uniqueIPv4AddressNum": len(self.ipv4AddressSet),
            "uniqueIPv6AddressNum": len(self.ipv6AddressSet),
            "uniqueEmailAddressNum": len(self.emailAddressSet),
            "uniqueDomainNum": len(self.domainSet),
            "uniqueUriNum": len(self.uriSet),
            "uniqueMatchIPv4AddressNum": len(self.matchIPv4AddressSet),
            "uniqueMatchIPv6AddressNum": len(self.matchIPv6AddressSet),
            "uniqueMatchEmailAddressNum": len(self.matchEmailAddressSet),
            "uniqueMatchDomainNum": len(self.matchDomainSet),
            "uniqueMatchUriNum": len(self.matchUriSet),

            "startTime": self.startTime,
            "endTime": self.endTime,
            "emailRecords": emailRecordsDict,
            "fileHashRecords": fileHashRecordsDict,
            "httpRecords": httpRecordsDict,
            "domainRecords": domainRecordsDict,
        }

    def __init__(self):
        self.totalPacket = 0  # Total packet num in pcap file
        self.totalIPAddress = 0  # Total ipv4 address num in pcap file
        self.totalIPv6Address = 0  # Total ipv6 address num in pcap file
        self.totalEmailAddress = 0  # Total email address num in pcap file
        self.totalIPPacket = 0  # Total ipv4 packet num in pcap file
        self.totalIPv6Packet = 0  # Total ipv6 pcaket num in pcap file
        self.duration = 0  # The duration between the begin of pcap file and end of pcap file
        self.totalTCPFlowNum = 0  # Total TCP flow num in pcap file
        self.totalHTTPNum = 0  # Total HTTP session num in pcap file
        self.totalFTPNum = 0  # Total FTP session num in pcap file
        self.totalEmailNum = 0  # Total email num in pcap file，contain SMTP、POP3 and IMAP protocol
        self.totalFileNum = 0  # Total file num extract from pcap file, from FTP、SMTP、POP3 、IMAP and HTTP
        self.totalDomainNum = 0  # Total domain num extract from DNS query and DNS response）

        self.totalMatchIpAddress = 0  # Total ipv4 address matched
        self.totalMatchIpv6Address = 0  # Total ipv6 address matched
        self.totalMatchEmailNum = 0  # Total email matched
        self.totalMatchDomain = 0  # Total domain matched
        self.totalMatchFileHash = 0  # Total file hash matched
        self.totalMatchUri = 0  # Total match uri

        self.emailRecords = []  # contain all email which some observable match it
        self.fileHashRecords = []  # contain all FTP session which some observable match it
        self.httpRecords = []  # contain all HTTP session which some observable match it
        self.domainRecords = []  # contain all Domain query record which some observable match it
        # self.observablesMap = dict()  # 一个字典，用来保存 Observable => <observableId, observable>

        self.isFirst = True
        self.isDumpCsv = True

        self.ipv4AddressSet = set()
        self.ipv6AddressSet = set()
        self.emailAddressSet = set()
        self.uriSet = set()
        self.domainSet = set()

        self.matchIPv4AddressSet = set()
        self.matchIPv6AddressSet = set()
        self.matchEmailAddressSet = set()
        self.matchUriSet = set()
        self.matchDomainSet = set()

        self.startTime = 0
        self.endTime = 0
        self.outputCsvDir = "outputcsv"
        self.pcapFile = ""

        self.ipAddressCSVFile = None
        self.emailAddressCSVFile = None
        self.uriCSVFile = None
        self.fileHashCSVFile = None
        self.domainCSVFile = None

        self.ipAddressCSVWriter = None
        self.emailAddressCSVWriter = None
        self.uriCSVWriter = None
        self.fileHashCSVWriter = None
        self.domainCSVWriter = None

    def begin(self):
        """
        报告开始
        :return:
        """
        pass

    def addPacket(self, ethPacket: ethernet.Ethernet, timestamp: float):
        """
        每解析到一个以太网包，
        :return:
        """
        if self.isFirst:
            self.startTime = timestamp
            self.isFirst = False
        self.endTime = timestamp
        self.duration = self.endTime - self.startTime

        self.totalPacket += 1
        ipPacket = ethPacket.data
        if isinstance(ethPacket.data, ip.IP):
            # 如果是 IPv4 包
            self.totalIPPacket += 1
            self.ipv4AddressSet.add(inet_to_str(ipPacket.src))
            self.ipv4AddressSet.add(inet_to_str(ipPacket.dst))
            self.totalIPAddress = len(self.ipv4AddressSet)
        elif isinstance(ethPacket.data, ip6.IP6):
            self.totalIPv6Packet += 1
            self.ipv6AddressSet.add(inet_to_str(ipPacket.src))
            self.ipv6AddressSet.add(inet_to_str(ipPacket.dst))
            self.totalIPv6Address = len(self.ipv6AddressSet)
        else:
            return False

    def addTCPFlow(self, tcpFlow: TCPFlow):
        """
        每解析到一个 TCP 流就调用本回调
        :param tcpFlow:
        :return:
        """
        self.totalTCPFlowNum += 1

    def checkFileHashes(self, observables: [dict], tcpFlow: TCPFlow):
        """
        检查 observables 中是否包含文件Hash，主要是用于对 HTTP 和 Email 中的 FileHash 进行处理
        :param tcpFlow:
        :param observables:
        :return:
        """
        for observableItem in observables:
            if observableItem["observableType"] == "fileHash":
                fileHash = FileHash()
                fileHash.md5 = observableItem["md5"]
                fileHash.sha1 = observableItem["sha1"]
                fileHash.sha256 = observableItem["sha256"]
                self.saveFileHash(fileHash, tcpFlow, self.getBriefObservable(observableItem, False))

    def addEmail(self, mail: Mail, tcpFlow: TCPFlow, observables: [dict]):
        """
        每解析到一个 Email，就调用本方法
        :param observables:
        :param mail:
        :param tcpFlow:
        :return:
        """
        self.totalEmailNum += 1
        self.emailAddressSet.add(mail.From)
        self.emailAddressSet.add(mail.To)
        self.totalEmailAddress = len(self.emailAddressSet)
        self.totalFileNum += len(mail.files)
        if len(observables) <= 0:
            return
        self.checkFileHashes(observables, tcpFlow)
        observables = self.addObservable(observables)
        emailRecord = EmailRecord()
        emailRecord.initByMailAndObservable(mail)
        emailRecord.setTCP(tcpFlow)
        emailRecord.setObservables(observables)
        self.emailRecords.append(emailRecord)

    def addDNSRecord(self, item: DNSItem, observables: [dict]):
        """
        每解析到一个 DNSRecord，就调动本方法
        :param observables:
        :param item:
        :return:
        """
        self.totalDomainNum += 1
        self.domainSet.add(item.domain)
        if len(observables) <= 0:
            return
        observables = self.addObservable(observables)
        dnsRecord = DNSRecord()
        dnsRecord.initByDNSItem(item)
        dnsRecord.setObservables(observables)
        self.domainRecords.append(dnsRecord)

    def addHttp(self, httpData: HttpData, tcpFlow: TCPFlow, observables: [dict]):
        """
        每解析到一个 HttpData，就调用本方法
        :param observables:
        [
            {
                "observables":[

                ],
                "value":"a1621.g.akamai.net",
                "observableType": "domain"
            },
            {
                "observables":[

                ],
                "value":"23.15.7.104",
                "observableType": "address"
            }
        ]
        :param httpData:
        :param tcpFlow:
        :return:
        """
        self.totalHTTPNum += 1
        self.uriSet.add(httpData.getUrl())
        self.domainSet.add(httpData.getDomain())
        if httpData.getDomain() != "":
            self.totalDomainNum += 1
        if httpData.fileHashes:
            self.totalFileNum += 1
        if len(observables) <= 0:
            return
        self.checkFileHashes(observables, tcpFlow)
        observables = self.addObservable(observables)
        httpRecord = HTTPRecord(httpData)
        httpRecord.setTCP(tcpFlow)
        httpRecord.setObservables(observables)
        self.httpRecords.append(httpRecord)

    def saveFileHash(self, fileHash: FileHash, tcpFlow: TCPFlow, observables: [dict], filename=""):
        if not observables or len(observables) == 0:
            return
        fileHashRecord = FileHashRecord()
        fileHashRecord.fileHash = fileHash
        fileHashRecord.filename = filename
        fileHashRecord.setTCP(tcpFlow)
        fileHashRecord.setObservables(observables)
        self.fileHashRecords.append(fileHashRecord)

    def addFileHash(self, fileHash: FileHash, tcpFlow: TCPFlow, observables: [dict], filename=""):
        """
        每解析到一个 FTP 文件，就调用本方法
        :param filename:
        :param fileHash:
        :param observables:
        :param tcpFlow:
        :return:
        """
        self.totalFTPNum += 1
        self.totalFileNum += 1
        if len(observables) <= 0:
            return
        observables = self.addObservable(observables)
        self.saveFileHash(fileHash, tcpFlow, observables, filename)

    def getBriefObservable(self, observableItem: dict, needCount=True):
        """
        静态统计
        :param needCount:
        :param observableItem:      // 是否需要统计
        :return:
        """
        if observableItem["observableType"] == 'ipv4-addr':
            # ipv4
            if needCount and observableItem["knownThreats"] == 1:  # 只输出已知威胁
                self.totalMatchIpAddress += 1
                self.matchIPv4AddressSet.add(observableItem["value"])
        elif observableItem["observableType"] == 'ipv6-addr':
            # ipv6
            if needCount and observableItem["knownThreats"] == 1:  # 只输出已知威胁
                self.totalMatchIpv6Address += 1
                self.matchIPv6AddressSet.add(observableItem["value"])
        elif observableItem["observableType"] == 'e-mail':
            # email
            if needCount and observableItem["knownThreats"] == 1:  # 只输出已知威胁
                self.totalMatchEmailNum += 1
                self.matchEmailAddressSet.add(observableItem["value"])
        elif observableItem["observableType"] == "domain":
            # domain
            if needCount and observableItem["knownThreats"] == 1:  # 只输出已知威胁
                self.totalMatchDomain += 1
                self.matchDomainSet.add(observableItem["value"])
        elif observableItem["observableType"] == "uri":
            # uri
            if needCount and observableItem["knownThreats"] == 1:  # 只输出已知威胁
                self.totalMatchUri += 1
                self.matchUriSet.add(observableItem["value"])
        elif observableItem["observableType"] == "fileHash":
            # fileHash
            if needCount:
                self.totalMatchFileHash += 1

    def addObservable(self, observables: [dict]):
        """
        统计收到的 Observable 信息
        :param observables:
        [
            {
                "value":"a1621.g.akamai.net",
                "observableType": "domain"
            },
            {
                "value":"23.15.7.104",
                "observableType": "ipv4-addr"
            }
        ]
        :return:
        """
        for observableItem in observables:
            self.getBriefObservable(observableItem, True)
        return observables

    @staticmethod
    def _getOccurTimeObservableIdObservableUploadTime(timestamp: float, observable: dict):
        return datetime.datetime.fromtimestamp(timestamp).strftime(
            '%Y-%m-%d %H:%M:%S'), observable["stix_id"], datetime.datetime.fromtimestamp(
            observable["create_time"]).strftime(
            '%Y-%m-%d %H:%M:%S')

    class ObservableCSVStatisticsHelper:
        """
        一个对 Observable 出现频次进行静态统计的辅助类
        """

        def __init__(self, fileName):
            self.file = open(fileName, "w", newline='', encoding='utf8')
            self.csvWriter = csv.writer(self.file)
            self.statisticsDict = {}
            self.knownThreatsDict = {}

        def addObservable(self, observable: dict):
            if observable["value"] not in self.statisticsDict:
                self.statisticsDict[observable["value"]] = 0
                self.knownThreatsDict[observable["value"]] = observable["knownThreats"]
            self.statisticsDict[observable["value"]] += 1

        def addFileHashObservable(self, value: str, observable: dict):
            # print(value, " => ", observable)
            if value not in self.statisticsDict:
                self.statisticsDict[value] = 0
                self.knownThreatsDict[value] = observable["knownThreats"]
            self.statisticsDict[value] += 1

        def getCount(self, value: str):
            """
            根据 value 获取其统计值
            :param value:
            :return:
            """
            if value not in self.statisticsDict:
                return 0
            return self.statisticsDict[value]

        def getIsKnownThreats(self, value: str):
            if value not in self.knownThreatsDict:
                return 0
            return self.knownThreatsDict[value]

        def exportCSV(self):
            self.csvWriter.writerow([
                "Serial Number", "value", "knownThreats", "count",
            ])
            seq = 1
            for key, value in self.statisticsDict.items():
                self.csvWriter.writerow([
                    f"{seq}", key, self.getIsKnownThreats(key), f"{value}"
                ])
                seq += 1

            self.file.close()

        def exportFileHashCSV(self):
            self.csvWriter.writerow([
                "Serial Number", "md5", "sha1", "sha256", "knownThreats", "count",
            ])
            seq = 1
            for key, value in self.statisticsDict.items():
                hashes = key.split("-")
                if len(hashes) != 3:
                    continue
                self.csvWriter.writerow([
                    f"{seq}", hashes[0], hashes[1], hashes[2], 1, f"{value}"
                ])
                seq += 1

            self.file.close()

        def doMerge(self, detailFileName, mergeFileName, startValueIdx, endValueIdx):
            # merge detail and statistics csv table
            with open(detailFileName, "r", newline='', encoding='utf8') as detailFile:
                detailReader = csv.reader(detailFile)
                with open(mergeFileName, "w", newline='', encoding='utf8') as mergeFile:
                    mergeWriter = csv.writer(mergeFile)
                    seq = 0
                    # 先读取掉头部
                    mergeWriter.writerow(["Serial Number", *detailReader.__next__(), "count"])
                    lastV = ""
                    for row in detailReader:
                        v = "-".join(row[startValueIdx:endValueIdx])
                        if lastV != v:
                            lastV = v
                            seq += 1
                        mergeWriter.writerow([
                            str(seq), *row, self.getCount(v)
                        ])

    def _dealIPAddressCSV(self):
        """
        处理导出 IPAddress CSV
        :return:
        """

        def _isIpAddress(ob: dict):
            return ob['observableType'] == 'ipv4-addr' or ob['observableType'] == 'ipv6-addr'

        def _saveRecord(record, timestamp: float, ob: dict):
            if _isIpAddress(ob):
                ipAddressCSVWriter.writerow([
                    record.srcIP, record.dstIP, ob["value"],
                    ob["knownThreats"],
                    datetime.datetime.fromtimestamp(timestamp).strftime(
                        '%Y-%m-%d %H:%M:%S')
                ])
                ipAddressStatisticsHelper.addObservable(ob)

        ipAddressStatisticsHelper = Report.ObservableCSVStatisticsHelper(
            f"{self.outputCsvDir}/{self.pcapFile}-ip_address_statistics.csv")

        # ip info
        with open(f"{self.outputCsvDir}/{self.pcapFile}-ip_address_detail.csv", "w", newline='',
                  encoding='utf8') as ipAddressCSVFile:
            ipAddressCSVWriter = csv.writer(ipAddressCSVFile)
            ipAddressCSVWriter.writerow(
                ["srcIP", "dstIP", "value", "knownThreats", "occur time"]
            )
            # from dnsRecord
            for domainRecord in self.domainRecords:
                for observable in domainRecord.observables:
                    _saveRecord(domainRecord, domainRecord.timestamp, observable)

            # from FTPRecord
            for fileHashRecord in self.fileHashRecords:
                for observable in fileHashRecord.observables:
                    _saveRecord(fileHashRecord, fileHashRecord.endTime, observable)

            # from HTTPRecord
            for httpRecord in self.httpRecords:
                for observable in httpRecord.observables:
                    _saveRecord(httpRecord, httpRecord.endTime, observable)

            # from EmailRecord
            for emailRecord in self.emailRecords:
                for observable in emailRecord.observables:
                    _saveRecord(emailRecord, emailRecord.endTime, observable)

        ipAddressStatisticsHelper.exportCSV()
        ipAddressStatisticsHelper.doMerge(f"{self.outputCsvDir}/{self.pcapFile}-ip_address_detail.csv",
                                          f"{self.outputCsvDir}/{self.pcapFile}-ip_address_merge.csv", 2, 4)

    def _dealEmailAddressCSV(self):
        """
        处理导出 Email Address CSV
        :return:
        """

        emailAddressStatisticsHelper = Report.ObservableCSVStatisticsHelper(
            f"{self.outputCsvDir}/{self.pcapFile}-email_address_statistics.csv")

        with open(f"{self.outputCsvDir}/{self.pcapFile}-email_address_detail.csv", "w", newline='',
                  encoding='utf8') as emailAddressCSVFile:
            emailAddressCSVWriter = csv.writer(emailAddressCSVFile)
            emailAddressCSVWriter.writerow([
                "srcIP", "dstIP", "srcPort", "srcPort", "from", "to", "value", "knownThreats", "occur time"
            ])
            # from EmailRecord
            for emailRecord in self.emailRecords:
                for observable in emailRecord.observables:
                    if observable['observableType'] == 'e-mail':
                        emailAddressCSVWriter.writerow([
                            emailRecord.srcIP, emailRecord.dstIP, emailRecord.srcPort, emailRecord.dstPort,
                            emailRecord.From, emailRecord.To, observable["value"],
                            observable["knownThreats"],
                            datetime.datetime.fromtimestamp(emailRecord.endTime).strftime(
                                '%Y-%m-%d %H:%M:%S')
                        ])
                        emailAddressStatisticsHelper.addObservable(observable)

        emailAddressStatisticsHelper.exportCSV()
        emailAddressStatisticsHelper.doMerge(f"{self.outputCsvDir}/{self.pcapFile}-email_address_detail.csv",
                                             f"{self.outputCsvDir}/{self.pcapFile}-email_address_merge.csv", 6, 8)

    def _dealUriCSV(self):
        """
        处理导出 Uri CSV
        :return:
        """
        uriStatisticsHelper = Report.ObservableCSVStatisticsHelper(
            f"{self.outputCsvDir}/{self.pcapFile}-uri_statistics.csv"
        )

        with open(f"{self.outputCsvDir}/{self.pcapFile}-uri_detail.csv", "w", newline='',
                  encoding='utf8') as uriCSVFile:
            uriCSVWriter = csv.writer(uriCSVFile)
            uriCSVWriter.writerow([
                "srcIP", "dstIP", "srcPort", "dstPort", "value", "knownThreats", "occur time"
            ])
            for httpRecord in self.httpRecords:
                for observable in httpRecord.observables:
                    if observable['observableType'] == 'uri':
                        uriCSVWriter.writerow([
                            httpRecord.srcIP, httpRecord.dstIP, httpRecord.srcPort, httpRecord.dstPort,
                            observable["value"],
                            observable["knownThreats"],
                            datetime.datetime.fromtimestamp(httpRecord.endTime).strftime(
                                '%Y-%m-%d %H:%M:%S')
                        ])
                        uriStatisticsHelper.addObservable(observable)
        uriStatisticsHelper.exportCSV()
        uriStatisticsHelper.doMerge(f"{self.outputCsvDir}/{self.pcapFile}-uri_detail.csv",
                                    f"{self.outputCsvDir}/{self.pcapFile}-uri_merge.csv", 4, 6)

    def _dealFileHashCSV(self):
        """
        处理导出 File hash CSV
        :return:
        """
        fileHashStatisticsHelper = Report.ObservableCSVStatisticsHelper(
            f"{self.outputCsvDir}/{self.pcapFile}-file_hash_statistics.csv"
        )

        with open(f"{self.outputCsvDir}/{self.pcapFile}-file_hash_detail.csv", "w", newline='',
                  encoding='utf8') as fileHashCSVFile:
            fileHashCSVWriter = csv.writer(fileHashCSVFile)
            fileHashCSVWriter.writerow([
                "srcIP", "dstIP", "srcPort", "dstPort", "md5", "sha1", "sha256", "file name",
                "knownThreats", "occur time"
            ])
            for fileHashRecord in self.fileHashRecords:
                value = fileHashRecord.getValue()
                for observable in fileHashRecord.observables:
                    if observable['observableType'] == 'fileHash':
                        fileHashCSVWriter.writerow([
                            fileHashRecord.srcIP, fileHashRecord.dstIP, fileHashRecord.srcPort, fileHashRecord.dstPort,
                            observable["md5"], observable["sha1"], observable["sha256"], fileHashRecord.filename,
                            observable["knownThreats"],
                            datetime.datetime.fromtimestamp(fileHashRecord.endTime).strftime(
                                '%Y-%m-%d %H:%M:%S')
                        ])
                        fileHashStatisticsHelper.addFileHashObservable(value, observable)
        fileHashStatisticsHelper.exportFileHashCSV()
        fileHashStatisticsHelper.doMerge(f"{self.outputCsvDir}/{self.pcapFile}-file_hash_detail.csv",
                                         f"{self.outputCsvDir}/{self.pcapFile}-file_hash_merge.csv", 4, 8)

    def _dealDomainCSV(self):
        """
        处理导出 Domain CSV
        :return:
        """
        domainStatisticsHelper = Report.ObservableCSVStatisticsHelper(
            f"{self.outputCsvDir}/{self.pcapFile}-domain_statistics.csv"
        )

        with open(f"{self.outputCsvDir}/{self.pcapFile}-domain_detail.csv", "w", newline='',
                  encoding='utf8') as domainCSVFile:
            domainCSVWriter = csv.writer(domainCSVFile)
            domainCSVWriter.writerow([
                "srcIP", "dstIP", "srcPort", "dstPort", "value", "knownThreats", "occur time"
            ])
            # from Domain record
            for domainRecord in self.domainRecords:
                for observable in domainRecord.observables:
                    if observable["observableType"] == 'domain':
                        domainCSVWriter.writerow([
                            domainRecord.srcIP, domainRecord.dstIP, str(53), "",
                            observable["value"],
                            observable["knownThreats"],
                            datetime.datetime.fromtimestamp(domainRecord.timestamp).strftime(
                                '%Y-%m-%d %H:%M:%S')
                        ])
                        domainStatisticsHelper.addObservable(observable)

            # from http record
            for httpRecord in self.httpRecords:
                for observable in domainRecord.observables:
                    if observable["observableType"] == 'domain':
                        domainCSVWriter.writerow([
                            httpRecord.srcIP, httpRecord.dstIP, httpRecord.srcPort, httpRecord.dstPort,
                            observable["value"],
                            observable["knownThreats"],
                            datetime.datetime.fromtimestamp(httpRecord.endTime).strftime(
                                '%Y-%m-%d %H:%M:%S')
                        ])
                        domainStatisticsHelper.addObservable(observable)
        domainStatisticsHelper.exportCSV()
        domainStatisticsHelper.doMerge(f"{self.outputCsvDir}/{self.pcapFile}-domain_detail.csv",
                                       f"{self.outputCsvDir}/{self.pcapFile}-domain_merge.csv", 4, 6)

    def end(self):
        """
        报告结束
        self.emailRecords = []  # contain all email which some observable match it
        self.fileHashRecords = []  # contain all FTP session which some observable match it
        self.httpRecords = []  # contain all HTTP session which some observable match it
        self.domainRecords = []  #
        :return:
        """
        if self.isDumpCsv:
            pass
            if not os.path.exists(self.outputCsvDir):
                os.makedirs(self.outputCsvDir)
            self._dealIPAddressCSV()
            self._dealEmailAddressCSV()
            self._dealUriCSV()
            self._dealFileHashCSV()
            self._dealDomainCSV()
