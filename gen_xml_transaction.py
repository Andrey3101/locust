import xml.dom.minidom
import logging

class xml_gen():
    def __init__(self):
        self.log = logging.getLogger("xml_gen")

    def add_element(self, doc, namenode1, namespace, namenode2, text):
            namenode = doc.createElement(namespace + ":" + namenode2)
            if text != None:
                namenodeTextNode = doc.createTextNode(text)
                namenode.appendChild(namenodeTextNode)
            namenode1.appendChild(namenode)

    def get_text_node(self, xml_str, namespace, name):
        xml_obj = xml.dom.minidom.parseString(xml_str)
        value = xml_obj.getElementsByTagNameNS(namespace, name)[0].firstChild.nodeValue
        return value


    def AcceptorAuthorisationRequest(self, datetime, InitgPty, Mrchnt, POI_id, PAN, XpryDt, AddtlCardData, TxDtTm, TxRef, TxDtls):
        doc = xml.dom.minidom.Document()
        S = doc.createElementNS('http://schemas.xmlsoap.org/soap/envelope/', 'S:Envelope')
        S.setAttribute("xmlns:S", "http://schemas.xmlsoap.org/soap/envelope/")
        S.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")

        SOAP_ENV = doc.createElement('SOAP-ENV:Header')
        S_BODY = doc.createElement('S:Body')
        S.appendChild(SOAP_ENV)

        AcceptorAuthorisationRequest = doc.createElement('ns17:AcceptorAuthorisationRequest')
        AcceptorAuthorisationRequest.setAttribute("xmlns", "http://schemas.bssys.com/iso20022/service/common/v1")
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns17','http://schemas.bssys.com/iso20022/service/messages/v1')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns10' , 'urn:iso:std:iso:20022:tech:xsd:caaa.007.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns11' , 'urn:iso:std:iso:20022:tech:xsd:caaa.008.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns12' , 'urn:iso:std:iso:20022:tech:xsd:caaa.009.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns13' , 'urn:iso:std:iso:20022:tech:xsd:caaa.010.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns14' , 'urn:iso:std:iso:20022:tech:xsd:caaa.013.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns15' , 'urn:iso:std:iso:20022:tech:xsd:caaa.014.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns16' , 'urn:iso:std:iso:20022:tech:xsd:caaa.015.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns2' , 'urn:iso:std:iso:20022:tech:xsd:caaa.001.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns3' , 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns4' , 'urn:iso:std:iso:20022:tech:xsd:caaa.005.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns5' , 'urn:iso:std:iso:20022:tech:xsd:caaa.006.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns6' , 'urn:iso:std:iso:20022:tech:xsd:caaa.011.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns7' , 'urn:iso:std:iso:20022:tech:xsd:caaa.012.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns8' , 'urn:iso:std:iso:20022:tech:xsd:caaa.003.001.01')
        AcceptorAuthorisationRequest.setAttribute('xmlns:ns9' , 'urn:iso:std:iso:20022:tech:xsd:caaa.004.001.01')
    
        AccptrAuthstnReq = doc.createElement('ns2:AccptrAuthstnReq')
        AcceptorAuthorisationRequest.appendChild(AccptrAuthstnReq)

        Hdr = doc.createElement('ns2:Hdr')
        AccptrAuthstnReq.appendChild(Hdr)
        self.add_element(doc, Hdr, 'ns2', 'MsgFctn', 'AUTQ')
        self.add_element(doc, Hdr, 'ns2', 'PrtcolVrsn', '01.00')
        self.add_element(doc, Hdr, 'ns2', 'XchgId', '0')
        self.add_element(doc, Hdr, 'ns2', 'CreDtTm', datetime)

        InitgPtyNode = doc.createElement('ns2:InitgPty')
        Hdr.appendChild(InitgPtyNode)
        self.add_element(doc, InitgPtyNode, 'ns2', 'Id', InitgPty)

        AuthstnReq = doc.createElement('ns2:AuthstnReq')
        AccptrAuthstnReq.appendChild(AuthstnReq)

        Envt = doc.createElement('ns2:Envt')
        AuthstnReq.appendChild(Envt)

        MrchntNode = doc.createElement('ns2:Mrchnt')
        Envt.appendChild(MrchntNode)
        MrchntIdNode = doc.createElement('ns2:Id')
        MrchntNode.appendChild(MrchntIdNode)
        self.add_element(doc, MrchntIdNode, 'ns2', 'Id', Mrchnt)

        POI = doc.createElement('ns2:POI')
        Envt.appendChild(POI)
        POIIdNode = doc.createElement('ns2:Id')
        POI.appendChild(POIIdNode)
        self.add_element(doc, POIIdNode, 'ns2', 'Id', POI_id)

        Card = doc.createElement('ns2:Card')
        Envt.appendChild(Card)
        PlainCardData = doc.createElement('ns2:PlainCardData')
        Card.appendChild(PlainCardData)
        self.add_element(doc, PlainCardData, 'ns2', 'PAN', PAN)
        self.add_element(doc, PlainCardData, 'ns2', 'XpryDt', XpryDt)
        self.add_element(doc, Card, 'ns2', 'CardPdctPrfl', '0060')
        self.add_element(doc, Card, 'ns2', 'AddtlCardData', AddtlCardData)

        Cntxt = doc.createElement('ns2:Cntxt')
        AuthstnReq.appendChild(Cntxt)
        PmtCntxt = doc.createElement('ns2:PmtCntxt')
        Cntxt.appendChild(PmtCntxt)
        self.add_element(doc, PmtCntxt, 'ns2', 'CardDataNtryMd', 'BRCD')
        SaleCntxt = doc.createElement('ns2:SaleCntxt')
        Cntxt.appendChild(SaleCntxt)

        Tx = doc.createElement('ns2:Tx')
        AuthstnReq.appendChild(Tx)
        self.add_element(doc, Tx, 'ns2', 'TxCaptr', 'true')
        self.add_element(doc, Tx, 'ns2', 'TxTp', 'CRDP')
        self.add_element(doc, Tx, 'ns2', 'SvcAttr', 'IRES')
        self.add_element(doc, Tx, 'ns2', 'MrchntCtgyCdTp', '5411')

        TxId = doc.createElement('ns2:TxId')
        Tx.appendChild(TxId)
        self.add_element(doc, TxId, 'ns2', 'TxDtTm', TxDtTm)
        self.add_element(doc, TxId, 'ns2', 'TxRef', TxRef)

        TxDtlsNode = doc.createElement('ns2:TxDtls')
        Tx.appendChild(TxDtlsNode)
        Ccy = TxDtls['Ccy']
        TtlAmt = TxDtls['TtlAmt']
        self.add_element(doc, TxDtlsNode, 'ns2', 'Ccy', str(Ccy))
        self.add_element(doc, TxDtlsNode, 'ns2', 'TtlAmt', str(TtlAmt))
        for TxDlsEl in TxDtls['Pdct']:
            Pdct = doc.createElement('ns2:Pdct')
            TxDtlsNode.appendChild(Pdct)
            self.add_element(doc, Pdct, 'ns2', 'PdctCd', str(TxDlsEl['PdctCd']))
            self.add_element(doc, Pdct, 'ns2', 'UnitOfMeasr', str(TxDlsEl['UnitOfMeasr']))
            self.add_element(doc, Pdct, 'ns2', 'PdctQty', str(TxDlsEl['PdctQty']))
            self.add_element(doc, Pdct, 'ns2', 'UnitPric', str(TxDlsEl['UnitPric']))
            self.add_element(doc, Pdct, 'ns2', 'PdctAmt', str(TxDlsEl['PdctAmt']))

        SctyTrlr = doc.createElement('ns2:SctyTrlr')
        AccptrAuthstnReq.appendChild(SctyTrlr)
        self.add_element(doc, SctyTrlr, 'ns2', 'CnttTp', 'DATA')

        S_BODY.appendChild(AcceptorAuthorisationRequest)
        S.appendChild(S_BODY)

        doc.appendChild(S)

        return(doc.toprettyxml(encoding='UTF-8'))


    def AcceptorBatchTransferRequest(self, datetime, InitgPty, Mrchnt, POI_id, PAN, XpryDt, AddtlCardData, TxDtTm, TxRef, TxDtls, Nm, code):

        doc = xml.dom.minidom.Document()
        S = doc.createElementNS('http://schemas.xmlsoap.org/soap/envelope/', 'S:Envelope')
        S.setAttribute("xmlns:S", "http://schemas.xmlsoap.org/soap/envelope/")
        S.setAttribute("xmlns:SOAP-ENV", "http://schemas.xmlsoap.org/soap/envelope/")

        SOAP_ENV = doc.createElement('SOAP-ENV:Header')
        S_BODY = doc.createElement('S:Body')
        S.appendChild(SOAP_ENV)

        AcceptorBatchTransferRequest = doc.createElement('ns17:AcceptorBatchTransferRequest')
        AcceptorBatchTransferRequest.setAttribute("xmlns", "http://schemas.bssys.com/iso20022/service/common/v1")
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns17','http://schemas.bssys.com/iso20022/service/messages/v1')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns10' , 'urn:iso:std:iso:20022:tech:xsd:caaa.007.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns11' , 'urn:iso:std:iso:20022:tech:xsd:caaa.008.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns12' , 'urn:iso:std:iso:20022:tech:xsd:caaa.009.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns13' , 'urn:iso:std:iso:20022:tech:xsd:caaa.010.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns14' , 'urn:iso:std:iso:20022:tech:xsd:caaa.013.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns15' , 'urn:iso:std:iso:20022:tech:xsd:caaa.014.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns16' , 'urn:iso:std:iso:20022:tech:xsd:caaa.015.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns2' , 'urn:iso:std:iso:20022:tech:xsd:caaa.001.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns3' , 'urn:iso:std:iso:20022:tech:xsd:caaa.002.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns4' , 'urn:iso:std:iso:20022:tech:xsd:caaa.005.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns5' , 'urn:iso:std:iso:20022:tech:xsd:caaa.006.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns6' , 'urn:iso:std:iso:20022:tech:xsd:caaa.011.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns7' , 'urn:iso:std:iso:20022:tech:xsd:caaa.012.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns8' , 'urn:iso:std:iso:20022:tech:xsd:caaa.003.001.01')
        AcceptorBatchTransferRequest.setAttribute('xmlns:ns9' , 'urn:iso:std:iso:20022:tech:xsd:caaa.004.001.01')
    
        AccptrBtchTrf = doc.createElement('ns6:AccptrBtchTrf')
        AcceptorBatchTransferRequest.appendChild(AccptrBtchTrf)

        Hdr = doc.createElement('ns6:Hdr')
        AccptrBtchTrf.appendChild(Hdr)
        self.add_element(doc, Hdr, 'ns6', 'DwnldTrf', 'false')
        self.add_element(doc, Hdr, 'ns6', 'FrmtVrsn', '01.00')
        self.add_element(doc, Hdr, 'ns6', 'XchgId', '45')
        self.add_element(doc, Hdr, 'ns6', 'CreDtTm', datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00')

        InitgPtyNode = doc.createElement('ns6:InitgPty')
        Hdr.appendChild(InitgPtyNode)
        self.add_element(doc, InitgPtyNode, 'ns6', 'Id', InitgPty)

        DataSet = doc.createElement('ns6:DataSet')
        AccptrBtchTrf.appendChild(DataSet)

        DataSetId = doc.createElement('ns6:DataSetId')
        DataSet.appendChild(DataSetId)
        self.add_element(doc, DataSetId, 'ns6', 'Nm', Nm)
        self.add_element(doc, DataSetId, 'ns6', 'Tp', 'TXCP')
        self.add_element(doc, DataSetId, 'ns6', 'CreDtTm', datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'+03:00')

        TxTtls = doc.createElement('ns6:TxTtls')
        DataSet.appendChild(TxTtls)
        Ccy = TxDtls['Ccy']
        summary = TxDtls['TtlAmt']
        self.add_element(doc, TxTtls, 'ns6', 'Ccy', str(Ccy))
        self.add_element(doc, TxTtls, 'ns6', 'Tp', 'DEBT')
        self.add_element(doc, TxTtls, 'ns6', 'TtlNb', '1')
        self.add_element(doc, TxTtls, 'ns6', 'CmltvAmt', str(summary))

        TxToCaptr = doc.createElement('ns6:TxToCaptr')
        DataSet.appendChild(TxToCaptr)
        self.add_element(doc, TxToCaptr, 'ns6', 'TxSeqCntr', '1')
        Envt = doc.createElement('ns6:Envt')
        TxToCaptr.appendChild(Envt)

        shop = doc.createElement('ns6:Mrchnt')
        Envt.appendChild(shop)
        merch_Id = doc.createElement('ns6:Id')
        shop.appendChild(merch_Id)
        self.add_element(doc, merch_Id, 'ns6', 'Id', Mrchnt)

        POI = doc.createElement('ns6:POI')
        Envt.appendChild(POI)
        POIIdNode = doc.createElement('ns6:Id')
        POI.appendChild(POIIdNode)
        self.add_element(doc, POIIdNode, 'ns6', 'Id', POI_id)

        Card = doc.createElement('ns6:Card')
        Envt.appendChild(Card)
        PlainCardData = doc.createElement('ns6:PlainCardData')
        Card.appendChild(PlainCardData)
        self.add_element(doc, PlainCardData, 'ns6', 'PAN', PAN)
        self.add_element(doc, PlainCardData, 'ns6', 'XpryDt', XpryDt)
        self.add_element(doc, Card, 'ns2', 'CardPdctPrfl', '0060')
        self.add_element(doc, Card, 'ns2', 'AddtlCardData', AddtlCardData)

        Tx = doc.createElement('ns6:Tx')
        TxToCaptr.appendChild(Tx)
        self.add_element(doc, Tx, 'ns6', 'TxTp', 'CRDP')
        self.add_element(doc, Tx, 'ns6', 'SvcAttr', 'IRES')
        self.add_element(doc, Tx, 'ns6', 'MrchntCtgyCdTp', '5411')

        TxId = doc.createElement('ns6:TxId')
        Tx.appendChild(TxId)
        self.add_element(doc, TxId, 'ns6', 'TxDtTm', TxDtTm)
        self.add_element(doc, TxId, 'ns6', 'TxRef', TxRef)

        OrgnlTx = doc.createElement('ns6:OrgnlTx')
        Tx.appendChild(OrgnlTx)
        TxId = doc.createElement('ns6:TxId')
        OrgnlTx.appendChild(TxId)
        self.add_element(doc, TxId, 'ns6', 'TxDtTm', TxDtTm)
        self.add_element(doc, TxId, 'ns6', 'TxRef', TxRef)

        POIId = doc.createElement('ns6:POIId')
        OrgnlTx.appendChild(POIId)
        self.add_element(doc, POIId, 'ns6', 'Id', POI_id)
        self.add_element(doc, OrgnlTx, 'ns6', 'TxTp', 'CRDP')

        TxRslt = doc.createElement('ns6:TxRslt')
        OrgnlTx.appendChild(TxRslt)
        RspnToAuthstn = doc.createElement('ns6:RspnToAuthstn')
        TxRslt.appendChild(RspnToAuthstn)
        self.add_element(doc, RspnToAuthstn, 'ns6', 'Rspn', 'APPR')
        self.add_element(doc, TxRslt, 'ns6', 'AuthstnCd', code)
        self.add_element(doc, Tx, 'ns6', 'TxSucss', 'true')

        TxDtls = doc.createElement('ns6:TxDtls')
        Tx.appendChild(TxDtls)
        self.add_element(doc, TxDtls, 'ns6', 'Ccy', str(Ccy)) # Код соц программы
        self.add_element(doc,TxDtls, 'ns6', 'TtlAmt', str(summary)) # Общая сумма транзакции


        SctyTrlr = doc.createElement('ns6:SctyTrlr')
        AccptrBtchTrf.appendChild(SctyTrlr)
        self.add_element(doc, SctyTrlr, 'ns2', 'CnttTp', 'DATA')

        S_BODY.appendChild(AcceptorBatchTransferRequest)
        S.appendChild(S_BODY)

        doc.appendChild(S)

        return(doc.toprettyxml(encoding='UTF-8'))