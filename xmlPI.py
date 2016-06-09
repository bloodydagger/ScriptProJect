# -*- coding: cp949 -*-
#-*- coding: utf-8 -*- 
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree

##### global
xmlFD = -1
PIDoc = None

#### xml 관련 함수 구현
def LoadXMLFromFile():
    fileName = str(input ("please input file name to load :"))
    global xmlFD, PIDoc
    try:
        xmlFD = open(fileName)
    except IOError:
        print ("invalid file name or path")
    else:
        try:
            dom = parse(xmlFD)
        except Exception:
            print ("loading fail!!!")
        else:
            print ("XML Document loading complete")
            PIDoc = dom
            return dom
    return None

def BooksFree():
    if checkDocument():
        PIDoc.unlink()
        
def PrintDOMtoXML():
    if checkDocument():
        print(PIDoc.toxml())

def PrinttitleList(tags):
    global PIDoc
    if not checkDocument():
       return None
        
    response = PIDoc.childNodes
    msgBody = response[0].childNodes
    for perforList in msgBody:
        if perforList.nodeName == "msgBody":
            PI =perforList.childNodes
            for item in PI:
                if item.nodeName == "perforList":# 엘리먼트를 중 perforlist인 것을 골라 냅니다.
                    subitems = item.childNodes# book에 들어 있는 노드들을 가져옵니다.
                    for atom in subitems:
                        if atom.nodeName in tags:
                            print("title=",atom.firstChild.nodeValue)# 타이틀 목록을 출력 합니다.
                
def AddPI(PIdata):
     global PIDoc
     if not checkDocument() :
        return None
     
     # msg엘리먼트 생성
     newmsg=PIDoc.createElement("msgBody")
     #newmsg.setAttribute('msgBody', PIdata['msgBody'])
     
     
     # period 엘리먼트 생성
     newPI = PIDoc.createElement("perforList")
     #newPI.setAttribute('perforList', PIdata['perforList'])
     # Title 엘리먼트 생성
     seqEle = PIDoc.createElement("seq")
     seqEle.setAttribute("seq", PIdata["seq"])
     titleEle = PIDoc.createElement("title")
     titleEle.setAttribute("title", PIdata["title"])
     # 텍스트 노드 생성
     seqNode = PIDoc.createTextNode(PIdata["seq"])
     titleNode = PIDoc.createTextNode(PIdata["title"])
     
     
     
     
     # 텍스트 노드를 Title 엘리먼트와 연결
     try:
         titleEle.appendChild(titleNode)
         seqEle.appendChild(seqNode)
     except Exception:
         print ("text append child fail- please,check the parent element & node!!!")
         return None
     else:
         titleEle.appendChild(titleNode)
         seqEle.appendChild(seqNode)

     # Title,seq 엘리먼트를 period 엘리먼트와 연결.
     try:
         newPI.appendChild(titleEle)
         newPI.appendChild(seqEle)
         
     except Exception:
         print ("title append child fail- please,check the parent element & node!!!")
         return None
     else:
         newPI.appendChild(titleEle)
         newPI.appendChild(seqEle)

    #period 엘리먼트를 msgbody 엘리먼트와연결
     try:
         newmsg.appendChild(newPI)
         
     except Exception:
         print ("msg append child fail- please,check the parent element & node!!!")
         return None
     else:
         newmsg.appendChild(newPI)
    #period 엘리먼트를 msgbody 엘리먼트와연결
     try:
         response = PIDoc.firstChild
         
     except Exception:
         print ("response append child fail- please,check the parent element & node!!!")
         return None
     else:
         if response != None:
             response.appendChild(newmsg)



def SearchPITitle(keyword):
    global PIDoc
    retlist = []
    if not checkDocument():
        return None
        
    try:
        tree = ElementTree.fromstring(str(PIDoc.toxml()))
    except Exception:
        print ("Element Tree parsing Error : maybe the xml document is not corrected.")
        return None
    
    #get Book Element
    #hPIElements = tree.getiterator("msgbody")  # return list type
    PIElements = tree.getiterator("perforList")
    for item in PIElements:
        strTitle = item.find("title")
        strseq =item.find("seq")
        if (strTitle.text.find(keyword) >=0 ):
            retlist.append((strseq.text, strTitle.text))#item.attrib["seq"]
    
    return retlist

def MakeHtmlDoc(BookList):
    from xml.dom.minidom import getDOMImplementation
    #get Dom Implementation
    impl = getDOMImplementation()
    
    newdoc = impl.createDocument(None, "html", None)  #DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for bookitem in BookList:
        #create bold element
        b = newdoc.createElement('b')
        #create text node
        ibsnText = newdoc.createTextNode("ISBN:" + bookitem[0])
        b.appendChild(ibsnText)

        body.appendChild(b)
    
        # BR 태그 (엘리먼트) 생성.
        br = newdoc.createElement('br')

        body.appendChild(br)

        #create title Element
        p = newdoc.createElement('p')
        #create text node
        titleText= newdoc.createTextNode("Title:" + bookitem[1])
        p.appendChild(titleText)

        body.appendChild(p)
        body.appendChild(br)  #line end
         
    #append Body
    top_element.appendChild(body)
    
    return newdoc.toxml()


def printBookList(blist):
    for res in blist:
        print (res)
    
def checkDocument():
    global PIDoc
    if PIDoc == None:
        print("Error : Document is empty")
        return False
    return True
  