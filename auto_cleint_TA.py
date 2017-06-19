'''
updated on 2016-12-08

@author: huzhan2,taoqsun
'''

import socket
import os
import time
import string
import shutil
import sys
import subprocess
import zipfile
import urllib
import urllib2
from urllib2 import URLError
import json
import types

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

global result_folder_name
global target_dir 
global result_folder_path 

def ismacosx():
    if os.name.startswith('posix') and sys.platform.startswith('darwin'):
        return True
    
    return False

__ismacosx__ = ismacosx()
        
def getCurrentScriptPath():
    curPath = sys.path[0]
    if os.path.isfile(curPath):
        curPath = os.path.dirname(curPath)
    return curPath

def cprint(log):
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " -- " + str(log)

class TALog():
    logFile = getCurrentScriptPath() + os.sep + "auto_client_TA.log"
    
    @classmethod
    def cleanLogFile(cls):      
        file_handle = open(TALog.logFile,"wb")
        file_handle.write("")
        file_handle.close()
    
    @classmethod    
    def fdbg(cls,logInfo):
        """Write log into a file, log file is placed in location '../Logs/' and file name format is similar with '2012-5-28.log'
        @param log: log text
        @type log: string
        """
        file_handle = open(TALog.logFile,"a+")
        file_handle.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " -- " + str(logInfo) + "\n")
        file_handle.close()

def modifyLinuxFolderToWrite( folder):
        try:
            import platform
            if platform.system() == 'Linux':
                os.popen('chmod 777 -Rf %s' % folder)
            elif __ismacosx__:
                os.popen('chmod -Rf 777 "%s"' % folder)
        except Exception,e:
            cprint('chmod 777 ,exception message :' + str(e))    
            TALog.fdbg(str(e))        

def mountLinuxFolderToLocal(folder):
        try:
            import platform
            if platform.system() == 'Linux':
                os.popen('mount -t nfs 10.194.246.26:/vol_ta_data/spare/share/clientta /%s' % folder)
            elif __ismacosx__:
                cprint('mount on mac os x "%s"' % folder)
                subprocess.Popen('mount_smbfs //tanfs.eng.webex.com/engta/share/clientta %s' % folder,shell=True).wait()
                cprint('mount compelted')
        except Exception,e:
            cprint('mount tanfs.eng.webex.com, exception message: ' + str(e))    
            TALog.fdbg(str(e))

class RequestWithMethod(urllib2.Request):
    def __init__(self,method,*args, **kwargs):
        self._method = method
        urllib2.Request.__init__(self,*args,**kwargs)

    def get_method(self):
        return self._method
    
class taMachine:
    def __init__(self,number,name = '',category = '',duration = 60,os= 'WIN7-32bit',pool= 'all' ):
        if  not isinstance(number,types.IntType) \
           or not isinstance(name,types.StringType) \
           or not isinstance(category,types.StringType) \
           or not isinstance(duration,types.IntType) \
           or not isinstance(os,types.StringType) \
           or not isinstance(pool,types.StringType):
            raise TypeError('Invalid data type in construct object')
        
        if number <= 0 or  duration <= 0:
            raise ValueError('In valid data value specified')
        
        self.__requestURL = 'http://taservice.eng.webex.com/taservice/resource/agent'
        self._taskName = name
        self._category = category
        self._duration = duration
        self._agentNum = number 
        self._osType = os
        self._agentPool = pool      

        self._taskID = '0'
        self.__machines = []

    def __del__(self):
        try:
            if self.__taskID != '0':
                self.putBackToPool()
                self.__taskID = '0'
        except Exception:
            pass
            
    def changeRequestURL(self,new_URL):
        if isinstance(new_URL,types.StringType) and '' != new_URL:
            self.__requestURL = new_URL
            return True

        return False
    
    def request(self):
        bRet = False
        json_data = '{"name":"%s","category":"%s","duration":"%s","number":"%d","os":"%s","pool":"%s"}' \
                    % (self._taskName,self._category,self._duration,self._agentNum,self._osType,self._agentPool)
        req = RequestWithMethod('POST',url=self.__requestURL,data = json_data, headers={"Content-Type":"application/json"})     
        try:
            u = urllib2.urlopen(req)
            creationResp = json.loads(u.read())
            cprint("request response :"+ os.linesep + str(creationResp))
            if creationResp['number'] == self._agentNum:
                self.__taskID = creationResp['taskid']
                cprint( 'Current task id of booking machine : ' + str(self.__taskID))
                if creationResp.get("machines")!=None:
                    for machine in creationResp['machines']:
                        self.__machines.append( machine )
                    bRet = True
            u.close()
                
        except URLError:
            
            pass
    
        return bRet

    def putBackToPool(self):
        req = RequestWithMethod('PUT',url=self.__requestURL + '/%s' % self.__taskID)
        try:
            urllib2.urlopen(req)
            self.__taskID = '0'
            return True
        
        except URLError:
            pass
        
        return False
        
    def getIPAddresses(self):
        ips = []
        ip_str = 'Booked machines (Total %d) : ' % len(self.__machines) + os.linesep
        hostname_str = "the hostname of Booked machines : " + os.linesep
        for machine in self.__machines:
            ip_str = ip_str + machine['ip'] + '\n'
            hostname_str = hostname_str + machine['hostname'] + '\n'
            ips.append(machine['ip'])
            
        cprint( ip_str )
        cprint(hostname_str)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        file_handle = open(target_dir + os.sep + "machine_information.txt","a+")
        file_handle.writelines(ip_str + hostname_str)
        file_handle.close()
        
        return ips
               
def runSTAFCmd(stafCmd,timeOutValue = 60):
    try:
        if __ismacosx__:           
            p = subprocess.Popen('declare -x DYLD_LIBRARY_PATH="/Users/admin/Library/staf/lib";' + stafCmd, bufsize = -1,shell=True,stdout=subprocess.PIPE)
            (stdoutdata, stdindata) = p.communicate(None)
#             p.wait()
            return stdoutdata
        else:
#             TALog.fdbg(stafCmd)
#             ret = os.popen(stafCmd).readlines()
            p = subprocess.Popen(stafCmd, shell=True)
            
            timeOut = 0
            ret = None
            while ret == None and timeOut <= timeOutValue:
                ret = p.poll()
                time.sleep(1)
                timeOut = timeOut + 1
            if timeOut > timeOutValue :
                cprint("runSTAFCmd : \"" + stafCmd +"\" time out ....") 
            
#             ret = p.wait()
            TALog.fdbg(str(ret))
            return ret
    except Exception,e:
        cprint('run staf command line,exception message :' + str(e))
        TALog.fdbg(str(e))
        
def copyDirToRemoteMachine(srcDir, dstDir, remoteIP):
    stafCmd = 'staf local fs copy DIRECTORY "%s" TODIRECTORY "%s" TOMACHINE %s RECURSE' % (srcDir, dstDir, remoteIP)
    cprint( stafCmd )
    bRet = True
    try:
        ret = runSTAFCmd(stafCmd)
#         TALog.fdbg(str(ret))
    except Exception,e:
        TALog.fdbg(str(e))
#         cprint( e )
        bRet = False
    return bRet

def copyFileToRemoteMachineDir(srcFile, dstDir, remoteIP):
    stafCmd = 'staf local fs copy file "%s" TODIRECTORY "%s" TOMACHINE %s' % (srcFile, dstDir, remoteIP)
    cprint( stafCmd )
    bRet = True
    try:
        ret = runSTAFCmd(stafCmd)
#         TALog.fdbg(str(ret))
    except Exception,e:
        TALog.fdbg(str(e))
#         cprint( e )
        bRet = False
    return bRet

def removeAllFilesAndDirInDir(targetDir, exceptFolderNameList = []): 
    if not os.path.exists(targetDir):
        msg = targetDir + ' not exist'
        cprint( msg )
        TALog.fdbg(msg)
        return
    try:
        for f in os.listdir(targetDir):
            targetFile = os.path.join(targetDir,  f)
            if os.path.isfile(targetFile):  
                os.remove(targetFile)  
            if os.path.isdir(targetFile) and f not in exceptFolderNameList:
                shutil.rmtree(targetFile)
    except Exception, e:
#         cprint( e )  
        TALog.fdbg(str(e))
    

def unZipFile(srcZipFile,desfold):
    bRet = False
    unZipCmd = r'unzip -o -d %s %s' %(desfold,srcZipFile,)
    cprint( unZipCmd )
    p = subprocess.Popen(unZipCmd, shell=True) 
    ret = p.wait()
    if ret == 0:
        bRet = True
        cprint( 'unZipFile success' )
    else:
        cprint( 'unZipFile fail' )
    return bRet

def zipFile(zipName, srcDir):
    bRet = False
    unZipCmd = r'zip -q -r %s %s' %(zipName, srcDir)
    cprint( unZipCmd )
    p = subprocess.Popen(unZipCmd, shell=True) 
    ret = p.wait()
    if ret == 0:
        bRet = True
        cprint( 'zipFile success' )
    else:
        cprint( 'zipFile fail' )
    return bRet

def pyZipFile(src, dstZip):
    if os.path.exists(src):
        f = zipfile.ZipFile(dstZip,'w',zipfile.ZIP_DEFLATED)
        try:
            if os.path.isfile(src):
                f.write(src)               
            else:
                for dirpath, dirnames, filenames in os.walk(src):
                    for filename in filenames:
                        tempFile = os.path.join(dirpath,filename)
                        f.write(tempFile, arcname = tempFile[len(src):])
            cprint( 'pyZipFile zip file success' )
        except Exception,e:
            cprint( e )
            cprint( 'pyZipFile zip file fail' )
        finally:
            f.close()
    else:
        cprint( str(src) + ' not exist')

def pyUnZipFile(zipFile, dstDir):
    if os.path.exists(zipFile):                    
        zipFile = zipfile.ZipFile(zipFile)
        try:
            NameList = zipFile.namelist()
            for nameItem in NameList:
                zipFile.extract(nameItem, dstDir)
            cprint( 'pyUnZipFile zip file success' )
        except Exception,e:
            cprint( e )
            cprint( 'pyUnZipFile zip file fail' )
        finally:
            zipFile.close()
    else:
        cprint( str(zipFile) + 'not exist')    
        
def deleteDir(targetDir):
    cprint( 'deleteDir...' + str(targetDir) )
    try:
        if os.path.exists(targetDir):
            shutil.rmtree(targetDir)
    except Exception, e:
        cprint( e )   
    cprint( 'deleteDir success' )

def deleteFile(targetFile):
    cprint( 'deleteFile... ' + str(targetFile))
    if os.path.exists(targetFile):
        os.remove(targetFile)
    cprint( 'deleteFile success')
    
def coverFiles(sourceDir,  targetDir, exceptSuffixList = [], exceptFolderNameList = []):
    try:
        #print '[coverFiles]enter dir  ' + sourceDir + ' start...'
        if not os.path.exists(targetDir):
            #print 'coverFiles() -> target dir not exist "%s", create new one' % targetDir
            os.makedirs(targetDir)
        for f in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir,  f)
            targetFile = os.path.join(targetDir,  f) 
            #cover the files
            if os.path.isfile(sourceFile) and sourceFile.split('.')[-1] not in exceptSuffixList:
                open(targetFile, "wb").write(open(sourceFile, "rb").read())
                #shutil.copy(sourceFile, targetFile)
            if os.path.isdir(sourceFile) and f not in exceptFolderNameList:
                coverFiles(sourceFile, targetFile, exceptSuffixList, exceptFolderNameList)
        #print '[coverFiles]leave dir ' + sourceDir + ' end'
    except Exception, e:
        print e

def copyFile(srcFile, dstFile):
#     cprint( 'copyFile: from %s --> %s' % (srcFile, dstFile)
    try:
        if os.path.exists(srcFile):
            open(dstFile, "wb").write(open(srcFile, "rb").read())
    except Exception, e:
        TALog.fdbg('copyFile except:' + str(e))
#         print e    
#     print 'copyFile success'
        
class AutoRunTA():
#     configFileName,RepoName,disableRestart,BUILDOPTION,
#                        componentName,siteURL,siteName,userName,userPasswd,excludedSuites
    def __init__(self,configFileName,RepoName,disableRestart,BUILDOPTION,BUILDNUMBER,BUILDVERSION,
                 componentName,siteURL,siteName,userName,userPasswd,excludedSuites):
        self.trunkTAPath = ""
        self.serverSharePath = ""
        self.managerJobPath = ""
        self.managerStartClientPath = ""
        self.managerSharePath = ""
        self.jobInfoDispatchDict = {}
        self.reportResultDict = {}
        self.reportPath = ""
        self.autoTATimeout = 30
        
        self.ipList = []
        self.ippoolGroupList = []
        self.roleList = []
        self.distributelibFlag = "true"
        self.caseTimeout = "300000"
        self.conditionBreakLogic = "1"
        
        self.configFileName = configFileName
        self.RepoName = RepoName
        self.disableRestart = disableRestart
        self.BUILDOPTION = BUILDOPTION
        self.BUILDNUMBER = BUILDNUMBER
        self.BUILDVERSION = BUILDVERSION
        self.componentName = componentName
        
        self.siteURL = siteURL
        self.siteName = siteName
        self.userName = userName
        self.userPasswd = userPasswd
        self.excludedSuites = excludedSuites
        
        self.tempJobPath = ""
        TALog.cleanLogFile()
        self.mbZipList = []
        self.caseFolderName = ""
        self.relativeSuitPath = ""
        self.suiteNumber = 0
        self.specificSuiteList = []
        self.isGotoBTS = False
        self.oGetMachine = None
    
    def __getXMLElemInfo(self, root, elemFlag, defaultValue = None):
        elem = root.find(elemFlag)
        if elem is not None and elem.text is not None:
            return elem.text
        else:
            return defaultValue  
        
    def __appendSubItemToListByParentFlag(self, root, ParentFlag, subItemFlag, dstList):
        try:
            parent = root.find(ParentFlag)
            if parent is not None:    
                for subItem in parent.iter(subItemFlag):
                    dstList.append(subItem.text)
        except Exception,e:
            print "exception"+str(e)
          
    def __readConfigInfo(self, configFileName):
        trunkTAPathFlag = 'trunkTAPath'
        ippoolFlag = 'ippool'
        ipFlag = 'ip'
        rolelistFlag = 'rolelist'
        roleFlag = 'role'
        distributelibFlag = 'distributelibFlag'
        caseTimeoutFlag = 'caseTimeout'
        conditionBreakLogicFlag = 'conditionBreakLogic' 
        autoTATimeoutFlag = 'autoTATimeout'
        managerJobPathFlag = 'managerJobPath'
        managerStartClientPathFlag = 'managerStartClientPath'
        managerSharePathFlag = 'managerSharePath'
        serverSharePathFlag = 'serverSharePath'
        mbZipListFlag = 'mbZipList'
        mbZipFileNameFlag = 'mbZipFileName'
        caseDirectoryStructureFlag = 'caseDirectoryStructure'
        caseFolderNameFlag = 'caseFolderName'
        relativeSuitPathFlag = 'relativeSuitPath'
        specificSuiteFlag = 'specificSuite'
   
        bRet = True            
        try:
            tree = ET.parse(configFileName)
            root = tree.getroot()
            
            #self.trunkTAPath = self.__getXMLElemInfo(root, trunkTAPathFlag, self.trunkTAPath)
            self.trunkTAPath = getCurrentScriptPath()
            cprint( 'current trunkTAPath = ' + str(self.trunkTAPath))
            self.distributelibFlag = self.__getXMLElemInfo(root, distributelibFlag, self.distributelibFlag)
            self.caseTimeout = self.__getXMLElemInfo(root, caseTimeoutFlag, self.caseTimeout)
            self.conditionBreakLogic = self.__getXMLElemInfo(root, conditionBreakLogicFlag, self.conditionBreakLogic)
            taTimeoutValue = self.__getXMLElemInfo(root, autoTATimeoutFlag, None)
            if taTimeoutValue != None:
                self.autoTATimeout = string.atoi(taTimeoutValue)
            self.managerJobPath = self.__getXMLElemInfo(root, managerJobPathFlag, self.managerJobPath)
            self.managerStartClientPath = self.__getXMLElemInfo(root, managerStartClientPathFlag, self.managerStartClientPath)
            self.managerSharePath = self.__getXMLElemInfo(root, managerSharePathFlag, self.managerSharePath)
            self.serverSharePath = self.__getXMLElemInfo(root, serverSharePathFlag, self.serverSharePath)
            caseDirRoot = root.find(caseDirectoryStructureFlag)
            self.__appendSubItemToListByParentFlag(root, mbZipListFlag, mbZipFileNameFlag, self.mbZipList)
            self.relativeSuitPath = self.__getXMLElemInfo(caseDirRoot, relativeSuitPathFlag, self.relativeSuitPath)
            
            self.__calcSuiteNumber(self.trunkTAPath + os.sep + self.relativeSuitPath)
            self.__appendSubItemToListByParentFlag(root, rolelistFlag, roleFlag, self.roleList)
            self.__appendSubItemToListByParentFlag(root, ippoolFlag, ipFlag, self.ipList)
            if len(self.ipList) == 0:
                cprint( "Can't read ip list from config file ,try to call GetIpList API " )
                self.isGotoBTS = True
                self.oGetMachine = taMachine(self.suiteNumber*len(self.roleList),'client ta name', 'client', 60, 'WIN7-32bit','client_pipeline')
                self.oGetMachine.request()
                self.ipList = self.oGetMachine.getIPAddresses()
                if len(self.ipList) == 0:
                    raise "Can't get machine from machine pool by call GetIpList API" 
            
            self.caseFolderName = self.__getXMLElemInfo(caseDirRoot, caseFolderNameFlag, self.caseFolderName)
            specificSuiteString = None
            specificSuiteString = self.__getXMLElemInfo(caseDirRoot, specificSuiteFlag, specificSuiteString)
            if specificSuiteString is not None and isinstance(specificSuiteString, str):
                self.specificSuiteList = specificSuiteString.split(";")
           
        except Exception,e:
            cprint( e )
            cprint( ', or xml document format error' )
            TALog.fdbg(str(e) + ', or xml document format error')
            bRet = False 
        cprint( 'read configuration complete'  )                                              
        return bRet
          
    def __generateIPPoolGroupList(self):
        bRet = True
        try:
            roleCount = len(self.roleList)
            ipCount = len(self.ipList) / roleCount * roleCount
            i = 0
            while i < ipCount:
                ippoolList = []
                for role in self.roleList:
                    ippoolList.append([role, self.ipList[i]])
                    i += 1
                self.ippoolGroupList.append(ippoolList)
        except Exception,e:
            TALog.fdbg(str(e))            
            bRet = False
        cprint( 'generate ip pool group list completed' )
        return bRet
        
    def __generateMBJobInfoFile(self, jobFile, jobName, workPath, casefileList, ippoolList, distributelibFlag = 'true',caseTimeout = '3600000', conditionBreakLogic = '1'):
        f = file(jobFile, 'w') # open for 'w'riting
        try:  
            f.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>")
            f.write("\n")
            f.write("<localjobs>")
            f.write("\n")
            f.write("<job>")
            f.write("\n")
            f.write("<product>MagicBoat</product>")
            f.write("\n")
            f.write("<name>%s</name>" % jobName)
            f.write("\n")
            f.write("<worklocation>%s</worklocation>" % workPath)
            f.write("\n")
            f.write("<!-- The case should be located in work location.  -->")
            f.write("\n")
            f.write("<caselist>")
            f.write("\n")
            for casefile in casefileList:
                f.write(casefile)
                f.write("\n")        
            f.write("</caselist>")
            f.write("\n")
            f.write("<maillist>your_mail@cisco.com</maillist>")
            f.write("\n") 
            f.write("<ConditionalBreakLogic>%s</ConditionalBreakLogic>" % conditionBreakLogic)
            f.write("\n")
            f.write("<distributelib>%s</distributelib>" % distributelibFlag)
            f.write("\n")
            f.write("<!-- minutes -->")
            f.write("\n")
            f.write("<timeout>%s</timeout>" % caseTimeout)
            f.write("\n")
            f.write("<ippool count=\"%d\" mode=\"manual\">" % len(ippoolList))
            f.write("\n")
            for ipinfo in ippoolList:
                f.write("<ip role=\"%s\" address=\"%s\"/>" % (ipinfo[0],ipinfo[1]))
                f.write("\n")
            f.write("</ippool>")
            f.write("\n")
            f.write("<ownermail>your_mail@cisco.com</ownermail>")
            f.write("\n")
            f.write("<global_variables>")
            f.write("\n")
            f.write("<variable name=\"client_log_dir\">"+ result_folder_path +"</variable>")
            f.write("\n")
            if "" !=  self.RepoName:
                f.write("<variable name=\"curreponame\">"+self.RepoName+"</variable>")
                f.write("\n")
            if "" !=  self.BUILDOPTION:
                f.write("<variable name=\"BUILDOPTION\">"+self.BUILDOPTION+"</variable>")
                f.write("\n")
            if "" !=  self.BUILDNUMBER:
                f.write("<variable name=\"BUILDNUMBER\">"+self.BUILDNUMBER+"</variable>")
                f.write("\n")
            if "" !=  self.BUILDVERSION:
                f.write("<variable name=\"BUILDVERSION\">"+self.BUILDVERSION+"</variable>")
                f.write("\n")
            if "" !=  self.siteURL:
                f.write("<variable name=\"site_url\">"+self.siteURL+"</variable>")
                f.write("\n")
            if "" !=  self.siteName:    
                f.write("<variable name=\"site_name\">"+self.siteName+"</variable>")
                f.write("\n")
            if "" !=  self.userName:
                f.write("<variable name=\"site_login_account\">"+self.userName+"</variable>")
                f.write("\n")
            if "" !=  self.userPasswd:
                f.write("<variable name=\"site_login_password\">"+self.userPasswd+"</variable>")
                f.write("\n")
            
            f.write("</global_variables>")
            f.write("\n")
            f.write("</job>")
            f.write("\n")
            f.write("</localjobs>")
        
        except Exception,e:
            TALog.fdbg(str(e))
        finally:
            if f != None:
                f.close()
    
    def __getCaseFileList(self, sourceFile, managerWorkPath):
        suiteCaseHead = "<case>"
        headPosition = len(suiteCaseHead)
        suiteCaseTail = "</case>"
        tailPosition = -len(suiteCaseTail)
        casefileList = []
        sourceFilePath = os.path.dirname(sourceFile)   
        fp = open(sourceFile)
        try:
            workPathName = managerWorkPath.split("\\")[-1]
            for line in fp:
                line = line.strip()
                if line.find(suiteCaseHead) != -1:
                    srcCaseFile = line[headPosition:tailPosition]
                    absSrcCaseFile = os.path.abspath(sourceFilePath + os.sep + srcCaseFile.replace('\\', '/'))
                    casepath = managerWorkPath + absSrcCaseFile[absSrcCaseFile.find(workPathName)+len(workPathName):].replace('/', '\\')
                    casefile = "<casefile>%s</casefile>" % casepath
                    casefileList.append(casefile)                            
        except Exception,e:
            TALog.fdbg(str(e))
        finally:
            fp.close() # close the file
            
        return casefileList
    
    def __getlocalIP(self):
        try:
            SCOKET=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            SCOKET.connect(('8.8.8.8',80))
            (addr,port) = SCOKET.getsockname()
            SCOKET.close()
            return addr
        except socket.error:
            return "127.0.0.1"
        
    def __writeLocalMBConfigFile(self, mbJobConfigFile):
        bRet = True
        f = file(mbJobConfigFile, 'w') # open for 'w'riting
        try:
            f.write("<config>")
            f.write("\n")
            f.write("<jobInfo>")
            f.write("\n")
            for ip in self.jobInfoDispatchDict.keys():
                jobitem = ip + "=" + ";".join(self.jobInfoDispatchDict[ip])
                f.write("<jobItem>%s</jobItem>" % jobitem)
                f.write("\n")
            f.write("</jobInfo>") 
            f.write("\n")
            f.write("<returnReportPath>%s</returnReportPath>" % (self.reportPath + os.sep + self.componentName))    
            f.write("\n")
            f.write("<mbZipList>")
            f.write("\n")
            for mbZipFileName in self.mbZipList:
                f.write("<mbZipFileName>%s</mbZipFileName>" % mbZipFileName)    
                f.write("\n")
            f.write("</mbZipList>")
            f.write("\n")
            localIP = self.__getlocalIP()
            f.write("<returnReportIP>%s</returnReportIP>" % localIP)
            f.write("\n")
            f.write("<caseFolderName>%s</caseFolderName>" % self.caseFolderName)
            f.write("\n")
            f.write("</config>")         
            
        except Exception,e:
            TALog.fdbg(str(e))
            bRet = False
        finally:
            if f != None:
                f.close()
        return bRet
        
    def __generateMBJobInfoFileBySuiteFile(self, suiteFile, ippoolList, jobInfoDispatchDict, jobInfoFileName, jobInfoFileSavePath, managerWorkPath):
        try:
            casefileList = self.__getCaseFileList(suiteFile, managerWorkPath)
            jobName = os.path.basename(suiteFile).split('.')[0]  #f.split('.')[0]               
            if ippoolList[0][1] in jobInfoDispatchDict.keys():
                jobInfoDispatchDict[ippoolList[0][1]].append(jobInfoFileName)
            else:
                jobInfoDispatchDict[ippoolList[0][1]] = [jobInfoFileName]
            workPath = managerWorkPath
            jobFile = jobInfoFileSavePath + os.sep + jobInfoFileName
            self.__generateMBJobInfoFile(jobFile, jobName, workPath, casefileList,ippoolList, 
                                       self.distributelibFlag, self.caseTimeout, self.conditionBreakLogic)
        except Exception,e:
            TALog.fdbg("__generateMBJobInfoFileBySuiteFile exception: " + str(e))
    
    def __serviceSuiteJobInfo(self, currentParentPath, languageFlag, serviceFlag, L10NFlag, timeStr, ippoolList, jobInfoDispatchDict, jobInfoFileSavePath, managerWorkPath):
        for p in os.listdir(currentParentPath):
            subPath = os.path.join(currentParentPath, p)
            #do not find L10NFlag folder
            if os.path.isdir(subPath) and p.find(L10NFlag) < 0:
                for f in os.listdir(subPath):
                    suitFile = os.path.join(subPath, f)
                    fileNameParseList = f.split('.')[0].split('_')
                    
                    if os.path.isfile(suitFile) and fileNameParseList[0] == serviceFlag and \
                        fileNameParseList[-1] == L10NFlag and suitFile.split('.')[-1] == 'suite':                            
                        jobName = f.split('.')[0]
                        jobInfoFileName = timeStr + "_%s_%s.txt" % (jobName, languageFlag)                                                          
                        self.__generateMBJobInfoFileBySuiteFile(suitFile, ippoolList, self.jobInfoDispatchDict, 
                                                                jobInfoFileName, jobInfoFileSavePath, managerWorkPath)
                        
    def __generateL10NJobInfoFiles(self, suitePath, jobInfoFileSavePath, managerWorkPath, suiteFolderName, L10NFlag):       
        bRet = True  
        try:
            if not self.isGotoBTS :
                serviceFlag = suiteFolderName.split('_')[-1]
            else:
                serviceFlag = suiteFolderName.split('_')[-2]
                
            currentParentPath = os.path.abspath(suitePath + os.sep + '..')
            currentDirInfoList = os.listdir(suitePath)
           
            for f in currentDirInfoList:
                if len(self.specificSuiteList) > 0 and f not in self.specificSuiteList:
                    continue
                sourceFile = os.path.join(suitePath, f)
                if os.path.isfile(sourceFile) and f.find('End') == -1 and sourceFile.split('.')[-1] == 'suite':
                    jobName = f.split('.')[0]
                    ippoolList = self.ippoolGroupList[self.suiteNumber % len(self.ippoolGroupList)]
                    timenow = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                    jobInfoFileName = timenow + "_%s.txt" % jobName                
                     
                    self.suiteNumber += 1                   
                    self.__generateMBJobInfoFileBySuiteFile(sourceFile, ippoolList, self.jobInfoDispatchDict, 
                                                            jobInfoFileName, jobInfoFileSavePath, managerWorkPath)                   
                    #add module suite
                    languageFlag = f.split('.')[0]
                    self.__serviceSuiteJobInfo(currentParentPath, languageFlag, serviceFlag, L10NFlag, timenow, ippoolList, 
                                               self.jobInfoDispatchDict, jobInfoFileSavePath, managerWorkPath)         
                    #add end meeting suite 
                    for checkFile in currentDirInfoList:
                        sourceFile = os.path.join(suitePath, checkFile)
                        if os.path.isfile(sourceFile) and checkFile.split('.')[-1] == 'suite' and checkFile.find('EndMeeting') > -1:                         
                            jobInfoFileName = timenow + "_%s_%s.txt" % (checkFile.split('.')[0], languageFlag) 
                            self.__generateMBJobInfoFileBySuiteFile(sourceFile, ippoolList, self.jobInfoDispatchDict, 
                                                                    jobInfoFileName, jobInfoFileSavePath, managerWorkPath)
                            break

        except Exception,e:
            TALog.fdbg(str(e))
            bRet = False
            
        return bRet
            
    def __generateAllSuitJobInfoFile(self, suitePath, jobInfoFileSavePath, managerWorkPath):
        bRet = True
        L10NFlag = 'L10N'
        try:
            for f in os.listdir(suitePath):
                sourceFile = os.path.join(suitePath, f)
                fName = f.split('.')[0]
                if 0 != len(self.excludedSuites):
                    if f in self.excludedSuites:
                        continue
                
                if os.path.isfile(sourceFile) and sourceFile.split('.')[-1] == 'suite' and fName.split('_')[-1] != L10NFlag :
                    if len(self.specificSuiteList) > 0 and f not in self.specificSuiteList:
                        continue
                    casefileList = self.__getCaseFileList(sourceFile, managerWorkPath)
                    jobName = f.split('.')[0]
                    ippoolList = self.ippoolGroupList[self.suiteNumber % len(self.ippoolGroupList)]
                    timenow = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                    jobFileName = timenow + "_%s.txt" % jobName                
                    if ippoolList[0][1] in self.jobInfoDispatchDict.keys():
                        self.jobInfoDispatchDict[ippoolList[0][1]].append(jobFileName)
                    else:
                        self.jobInfoDispatchDict[ippoolList[0][1]] = [jobFileName]
                    workPath = managerWorkPath
                    jobFile = jobInfoFileSavePath + os.sep + "%s" % jobFileName
                    self.__generateMBJobInfoFile(jobFile, jobName, workPath, casefileList,ippoolList, 
                                               self.distributelibFlag, self.caseTimeout, self.conditionBreakLogic)
                    self.suiteNumber += 1
                elif os.path.isdir(sourceFile):
                    bRet = self.__generateAllSuitJobInfoFile( sourceFile, jobInfoFileSavePath, managerWorkPath)
        except Exception,e:
            TALog.fdbg(str(e))
            bRet = False
            
        return bRet
    
    def __calcSuiteNumber(self,suitePath):
        bRet = True
        try:
            for f in os.listdir(suitePath):
                sourceFile = os.path.join(suitePath, f)
                if 0 != len(self.excludedSuites):
                    if f in self.excludedSuites:
                        continue
                    
                if os.path.isfile(sourceFile) and sourceFile.split('.')[-1] == 'suite' and sourceFile.split('_')[-1].strip() != 'L10N.suite': 
                    self.suiteNumber += 1
                elif os.path.isdir(sourceFile):
                    bRet = self.__calcSuiteNumber( sourceFile)
        except Exception,e:
            TALog.fdbg(str(e))
            bRet = False
            
        return bRet
    
    def __configSuitJobInfo(self, suitePath, jobInfoFileSavePath, managerWorkPath):
        bRet = True
        self.suiteNumber = 0
        self.jobInfoDispatchDict = {}
        for i in range(1):
            if not os.path.exists(suitePath):
                msg = 'suitePath = %s not exist' % suitePath
                cprint( msg )
                TALog.fdbg(msg) 
                break
            suiteFolderName = suitePath.replace('\\', '/').split('/')[-1]
            L10NFlag = 'L10N'
            if suiteFolderName.find(L10NFlag) != -1:
                bRet = self.__generateL10NJobInfoFiles(suitePath, jobInfoFileSavePath, managerWorkPath, suiteFolderName, L10NFlag)
                if bRet == False:
                    TALog.fdbg("__generateL10NJobInfoFiles fail: %s %s %s" % (suitePath, jobInfoFileSavePath, managerWorkPath))
                    break
            else:
                bRet = self.__generateAllSuitJobInfoFile(suitePath, jobInfoFileSavePath, managerWorkPath)
                if bRet == False:
                    TALog.fdbg("__generateAllSuitJobInfoFile fail: %s %s %s" % (suitePath, jobInfoFileSavePath, managerWorkPath))
                    break
        return bRet
        
    def __configLocalJobFile(self): 
        bRet = True
        try:  
            for i in range(1):
                self.reportPath = self.trunkTAPath + os.sep + "report"
                self.tempJobPath = self.trunkTAPath + os.sep + "client_mb_job"
                tempJobCasePath = self.tempJobPath + os.sep + self.caseFolderName
                casePath = self.trunkTAPath + os.sep + self.caseFolderName
                mbLocalJobCallPath = self.trunkTAPath + os.sep + "mbLocalJobCall"
                
                #check report path
                if not os.path.exists(self.reportPath + os.sep + self.componentName):
                    TALog.fdbg( 'Creating report folder:' + self.reportPath + os.sep + self.componentName )
                    os.makedirs(self.reportPath + os.sep + self.componentName)
                else:
                    TALog.fdbg('Report folder is already exist.')
                    
               
                #check svnMBLocalJobCallPath 
                if not os.path.exists(mbLocalJobCallPath):
                    msg = 'mbLocalJobCallPath: %s not exist' % mbLocalJobCallPath
                    cprint( msg )
                    TALog.fdbg(msg)
                    bRet = False
                    break
                                    
                #clean tempJobPath
                deleteDir(self.tempJobPath)
                #copy svnMBLocalJobCallFolder to tempJobPath
                exceptSuffixList = ['bak', 'java']
                coverFiles(mbLocalJobCallPath, self.tempJobPath, exceptSuffixList)
                
                exceptSuffixList = ['bak', 'xlsx']
                exceptFileNameList = ['.svn']
                coverFiles(casePath, tempJobCasePath, exceptSuffixList, exceptFileNameList)
                
                #copy zip to tempJobPath   
                for mbZipFileName in self.mbZipList:
                    srcZip = self.trunkTAPath + os.sep + mbZipFileName
                    dstZip = self.tempJobPath + os.sep + mbZipFileName
                    copyFile(srcZip, dstZip)    
                       
        except Exception,e:
            TALog.fdbg(str(e))
            bRet = False
        return bRet  
            
    def __checkReport(self):
        cprint('Waiting magicboat job complete...')
        intervalSeconds = 20
        totalSeconds = self.autoTATimeout * 60
        countSeconds = 0
        #check receive report
        bContinueCheck = False
        while countSeconds < totalSeconds: 
            TALog.fdbg(str(self.reportResultDict))
            TALog.fdbg("wait seconds = %d" % countSeconds)
            bContinueCheck = False
            curReportPath = self.reportPath + os.sep + self.componentName
            for f in os.listdir(curReportPath):
                sourceZip = os.path.join(curReportPath,  f)
                 
                #cover the files
                if os.path.isfile(sourceZip) :
                    if f.split(".")[-1] == "zip" :
                        try:
#                             unzip report zip files
                            pyUnZipFile(sourceZip,curReportPath)
                            sourceFile = os.path.join(curReportPath,  'report.xml')
                            targetFile = os.path.join(curReportPath,  f.split(".")[0] + ".xml")
                            open(targetFile, "wb").write(open(sourceFile, "rb").read())
                        except Exception,e:
                            TALog.fdbg(str(e))
                            continue
                        self.reportResultDict[f] = True
                        deleteFile(sourceZip)
                        deleteFile(sourceFile)
                    
                    #-->taoqsun 2016/03/01 add check log file logic to fix wait time too long bug.
                    if f.split(".")[-1] == "log" :
                        cprint('find ' + str(f) + ' file ,then set the suite status to True ...')
                        self.reportResultDict[f.split('.')[0] + ".zip"] = True
            
            for reportName in self.reportResultDict.keys():
                if self.reportResultDict[reportName] == False:
                    bContinueCheck = True
                    break
                
            if bContinueCheck == True:
                time.sleep(intervalSeconds)
                countSeconds += intervalSeconds
            else:
                break
        else:
            cprint("check report time out ...") 
                     
    def initCofig(self, configFile):
        bRet = False
        for i in range(1):
            bRet = self.__readConfigInfo(configFile)
            if bRet == False:
                TALog.fdbg("__readConfigInfo fail")
                break
            bRet = self.__generateIPPoolGroupList()
            if bRet == False:
                TALog.fdbg("__generateIPPoolGroupList fail")
                break

            bRet = self.__configLocalJobFile()
            if bRet == False:
                TALog.fdbg("__configLocalJobFile fail")
                break        
                
            tempSuitePath = self.tempJobPath + os.sep + self.relativeSuitPath.replace('\\', os.sep).replace('/', os.sep)
            managerWorkPath = self.managerJobPath + "\\" + self.caseFolderName
            mbJobConfigFile = self.tempJobPath + os.sep + "mbJobConfig.xml"
            bRet = self.__configSuitJobInfo(tempSuitePath, self.tempJobPath, managerWorkPath)
            if bRet == False:
                TALog.fdbg("__configSuitJobInfo fail %s %s %s" % (tempSuitePath, self.tempJobPath, managerWorkPath))
                break
            bRet = self.__writeLocalMBConfigFile(mbJobConfigFile)
            if bRet == False:
                TALog.fdbg("__writeLocalMBConfigFile fail")
                
            #zip cases folder
            #zipFile("./client_mb_job/cases.zip","./cases")
            tempCaseFolder = self.tempJobPath + os.sep + self.caseFolderName
            cprint( "create cases.zip .......")
            pyZipFile(tempCaseFolder, tempCaseFolder + ".zip")
            cprint( "create cases.zip finished .......")
            deleteDir(tempCaseFolder)
            
        return bRet
        
    def runTA(self): 
        TALog.fdbg(str(self.jobInfoDispatchDict))
        #clean reprot path
        exceptFolderNameList = ['.svn']
        removeAllFilesAndDirInDir(self.reportPath + os.sep + self.componentName, exceptFolderNameList)
        
        shareFolder = ""
        if self.configFileName != "":
            shareFolder += os.sep + self.configFileName
        shareFolder += os.sep + 'client_mb_job'
        serverShareFolder = self.serverSharePath + shareFolder
        managerShareFolder = self.managerSharePath + shareFolder
        serverShareFolder = serverShareFolder.replace('\\', '/')
        managerShareFolder = managerShareFolder.replace('\\', '/')
        
        #if not set share folder, send folder to manager machine
        if self.serverSharePath == "" or self.managerSharePath == "" or self.managerStartClientPath == "":
            for mbManagerIP in self.jobInfoDispatchDict.keys():
                #add report file flag
                for jobName in self.jobInfoDispatchDict[mbManagerIP]:
                    reportName = jobName.split('.')[0] + "_report.zip"
                    self.reportResultDict[reportName] = False
                #clean mb manager localJobPath
                stafDeleteFolderCMD = 'staf %s fs delete entry "%s" confirm recurse' %(mbManagerIP, self.managerJobPath)
                cprint( "delete the manage machine workspace... ")
                runSTAFCmd(stafDeleteFolderCMD)#first delete old folder
                
                cprint( "copy the job folders to remote ...")
                copyDirToRemoteMachine(self.tempJobPath, self.managerJobPath, mbManagerIP)
                cprint( "copy the job folders to remote finished ...")
                
                #start mb manager
                managerAutoMBClientFile = self.managerJobPath + "\\auto_MB_Client.py"
                stafStartMBCmd = 'staf %s process start command "python %s"' % (mbManagerIP, managerAutoMBClientFile)
                runSTAFCmd(stafStartMBCmd)
                cprint( "start to run auto_MB_Client.py ...")
        else:
            #clean serverShareFolder
            cprint( "delete the manage machine workspace ...")
            deleteDir(serverShareFolder)
            
            #copy local job folder to share path
            cprint( "copy the job folders to remote ...")
            copyDirToRemoteMachine(self.tempJobPath, serverShareFolder, 'local')
            
            #modify serverShareFolder to write privilege
            modifyLinuxFolderToWrite(serverShareFolder)
            #copy start_client.py to mb manager and run it
            for mbManagerIP in self.jobInfoDispatchDict.keys():
                #add report file flag
                for jobName in self.jobInfoDispatchDict[mbManagerIP]:
                    reportName = jobName.split('.')[0] + "_report.zip"
                    self.reportResultDict[reportName] = False
                #copy start_client.py to manager machine
                cprint( "copy the start_client.py to remote  ...")
                startClientFile =  self.trunkTAPath + os.sep + "start_client.py"
                copyFileToRemoteMachineDir(startClientFile, self.managerStartClientPath, mbManagerIP)
                cprint( "copy the start_client.py to remote finished ...")
                 
                #start start_client.py of manager machine
                managerStartFile = self.managerStartClientPath + "\\start_client.py"
                if self.disableRestart :
                    disableRestart = "true"
                    stafStartClientCmd = 'staf %s process start command "python %s %s %s %s"' % (mbManagerIP, managerStartFile, managerShareFolder, self.managerJobPath,disableRestart)
                else:
                    stafStartClientCmd = 'staf %s process start command "python %s %s %s"' % (mbManagerIP, managerStartFile, managerShareFolder, self.managerJobPath)
                runSTAFCmd(stafStartClientCmd)
                cprint( "start the start_client.py on remote  ...")
        
        #check report zip
        self.__checkReport()
        cprint( "all suites is finished on remote  ...")
        try:
            if not os.path.exists(target_dir + "/TALog"):
                os.makedirs(target_dir + "/TALog")
            coverFiles(self.reportPath, target_dir + "/TALog" , exceptSuffixList = ['xml'])
            modifyLinuxFolderToWrite(target_dir + "/TALog")
        except Exception,e:
            cprint('Exception occurred : %s' % str(e))
           
    def autoRun(self):
        for i in range(1):
            TALog.fdbg("length = "+str(len(sys.argv)))
            
#             if len(sys.argv) < 2:
#                 TALog.fdbg("please input auto_client_TA config parameter")
#                 break
#             
#             self.configFileName = sys.argv[1]
            configFile = getCurrentScriptPath() + os.sep + "%s.xml" % self.configFileName
#             
#             if len(sys.argv) > 2:
#                 self.RepoName=sys.argv[2]
#                 TALog.fdbg("Current Repo name is %s" % sys.argv[2])
#             else:
#                 self.RepoName="null"
#             
#             if len(sys.argv) > 3:
#                 if "true" == sys.argv[3]:
#                     self.disableRestart = True
#                     TALog.fdbg("Current disableRestart is %s" % sys.argv[3])
#             else:
#                 self.disableRestart = False
#             
#             if len(sys.argv) > 4:
#                 self.BUILDOPTION=sys.argv[4]
#                 TALog.fdbg("Current BUILDOPTION is %s" % sys.argv[4])
#             else:
#                 self.BUILDOPTION="null"
#             
#             if len(sys.argv) > 5:
#                 self.componentName=sys.argv[5]
#                 TALog.fdbg("Current Component name is %s" % sys.argv[5]) 
            cprint( "init config file...")
            
            bRet = self.initCofig(configFile)
            if bRet == False:
                TALog.fdbg("initCofig fail")
                break
            cprint( "init config file finished...")
            
            self.runTA()
            
            if self.isGotoBTS :
                cprint( 'put test agent back to machine pool')
                self.oGetMachine.putBackToPool()
            
if __name__ == "__main__":
#     mountLinuxFolderToLocal("TA_PIC2")
    #oGetMachine = taMachine(100,'client ta name', 'client', 60, 'WIN7-32bit','client_pipeline')
    #oGetMachine.request()
    if 0 == 0:
        cprint( "start to run auto_client_TA.py...")
        req_version = (2,7)
        print "current python version =",sys.version_info    
        if sys.version_info < req_version:
            import optparse   
            parser = optparse.OptionParser()
            parser.add_option("-configFileName", dest = "configFileName" ,type="string", 
                              action="store", help = "the name of config file")
            parser.add_option("-repoName", dest = "RepoName", type="string", 
                              action="store", help = "repo name")
            parser.add_option("-disableRestart", dest = "disableRestart", type="string", 
                              action="store", help = "whether to disable restart when job run failed or import Lib failed.")
            parser.add_option("-buildOption", dest = "buildOption", type="string", 
                              action="store", help = "buildOption" )
            parser.add_option("-buildNumber", dest = "buildNumber", type="string", 
                              action="store", help = "buildNumber" )
            parser.add_option("-buildVersion", dest = "buildVersion", type="string", 
                              action="store", help = "buildVersion" )
            parser.add_option("-componentName", dest = "componentName", type="string", 
                              action="store", help = "componentName" )
            parser.add_option("-siteURL", dest = "siteURL", type="string", 
                              action="store", help = "the site URL what you want to run" )
            parser.add_option("-siteName", dest = "siteName", type="string", 
                              action="store", help = "the site name what you want to run" )
            parser.add_option("-userName", dest = "userName", type="string", 
                              action="store", help = "the user name what you want to login" )
            parser.add_option("-userPasswd", dest = "userPasswd", type="string", 
                              action="store", help = "the user name what you want to login" )
            parser.add_option("-excludedSuites", dest = "excludedSuites", type="string", 
                              action="store", help = "the suite name what you don't want to run" )
            (args,values) = parser.parse_args()
    
        else:
            import argparse
            parser = argparse.ArgumentParser()
            parser.add_argument("-configFileName", dest = "configFileName" ,required=False, type=str, 
                                action="store", help = "the name of config file")
            parser.add_argument("-repoName", dest = "repoName",required=False, type=str, 
                                action="store", help = "repo name")
            parser.add_argument("-disableRestart", dest = "disableRestart",required=False, type=str, 
                                action="store", help = "whether to disable restart when job run failed or import Lib failed.")
            parser.add_argument("-buildOption", dest = "buildOption",required=False, type=str, 
                                action="store", help = "buildOption")
            parser.add_argument("-buildNumber", dest = "buildNumber",required=False, type=str, 
                                action="store", help = "buildNumber")
            parser.add_argument("-buildVersion", dest = "buildVersion",required=False, type=str, 
                                action="store", help = "buildVersion")
            parser.add_argument("-componentName", dest = "componentName",required=False, type=str, 
                                action="store", help = "componentName")
            parser.add_argument("-siteURL", dest = "siteURL",required=False, type=str, 
                                action="store", help = "the site URL what you want to run")
            parser.add_argument("-siteName", dest = "siteName",required=False, type=str, 
                                action="store", help = "the site name  what you want to run")
            parser.add_argument("-userName", dest = "userName",required=False, type=str, 
                                action="store", help = "the user name what you want to login")
            parser.add_argument("-userPasswd", dest = "userPasswd",required=False, type=str, 
                                action="store", help = "the user name what you want to login")
            parser.add_argument("-excludedSuites", dest = "excludedSuites",required=False, type=str, 
                                action="store", help = "the suite name what you don't want to run")
            args = parser.parse_args()
        
        #set default value for the blew parameter
        configFileName = ""
        RepoName = ""
        disableRestart = False
        BUILDOPTION = ""
        BUILDNUMBER = ""
        BUILDVERSION = ""
        componentName = ""
        siteURL = ""
        siteName = ""
        userName = ""
        userPasswd = ""
        excluded_suites = []
        
        if None != args.configFileName:
            configFileName = args.configFileName
        
        if None != args.repoName:
            RepoName = args.repoName
            result_folder_name = RepoName
        else:
            result_folder_name = configFileName
        
        if None != args.buildNumber:
            BUILDNUMBER = args.buildNumber
        
        if None == args.repoName and None != args.buildNumber:
#             print "this is a offical build...."
            linuxPath = "%s%s" % ("build/", BUILDNUMBER)
            result_folder_name = "%s%s" % ("build"+"\\", BUILDNUMBER) 
            
        if None != args.buildNumber and None != args.repoName:
#             print "this is a pipeline build...."
            linuxPath = "%s%s_%s" % ("gate/",result_folder_name, BUILDNUMBER)
            result_folder_name = "%s%s_%s" % ("gate"+"\\",result_folder_name, BUILDNUMBER)
        
        
        if configFileName.lower().find("go2bts") != -1 and None == args.repoName and None == args.buildNumber :
#             print "this is a gotoBTS build...."
            linuxPath = "%s%s_%s_%s" % ("GotoBTS/",result_folder_name, "GotoBTS", time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
            result_folder_name = "%s%s_%s_%s" % ("GotoBTS"+"\\",result_folder_name, "GoToBTS", time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
            
        if None == args.repoName and None == args.buildNumber and configFileName.lower().find("go2bts") == -1 :
#             print "this is a fullRun build...."
            linuxPath = "%s%s_%s_%s" % ("FullRun/",result_folder_name, "FullRun", time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
            result_folder_name = "%s%s_%s_%s" % ("FullRun"+"\\",result_folder_name, "FullRun", time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
         
            
        result_folder_path = "F:\\share\\clientta\\ClientLogs\\%s" % result_folder_name
        
        target_dir = '/TA_PIC2'
        if __ismacosx__:
            target_dir = '/Volumes/TA_PIC2'            
        
        try:      
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)        
                modifyLinuxFolderToWrite(target_dir)
            
            if len(os.listdir(target_dir)) == 0:
                mountLinuxFolderToLocal(target_dir)
                
            target_dir = target_dir + "/ClientLogs/%s" % linuxPath     
            if not os.path.exists(target_dir):
    #             print "target_dir = ",target_dir
                os.makedirs(target_dir)
                modifyLinuxFolderToWrite(target_dir) 
                TALog.fdbg("folder '%s' has been created for read and write." % target_dir)
            else:
                TALog.fdbg("folder '%s' already exist." % target_dir)
        except Exception,e:
            cprint('Exception occured: %s' % str(e))
            
        if None != args.disableRestart:
            if args.disableRestart.lower() == 'true':
                disableRestart = True
        
        if None != args.buildOption:
            BUILDOPTION = args.buildOption
        
        if None != args.buildVersion:
            BUILDVERSION = args.buildVersion
        
        if None != args.componentName:
            componentName = args.componentName
        
        if None != args.siteURL:
            siteURL = args.siteURL
            
        if None != args.siteName:
            siteName = args.siteName
        
        if None != args.userName:
            userName = args.userName
        
        if None != args.userPasswd:
            userPasswd = args.userPasswd
        
        if None != args.excludedSuites:
            _service_suite_map = {'mc':'mc.suite',
                                          'tc':'tc.suite',
                                          'ec':'ec.suite',
                                          'sc':'sc.suite'}
            service_names =  args.excludedSuites.split(',')
            for service_name in service_names:
                service_name = service_name.lower().strip()
                if _service_suite_map.has_key(service_name):
                    excluded_suites.append(_service_suite_map[service_name])                   
          
#         print "excluded_suites =",excluded_suites
        
        autoTA = AutoRunTA(configFileName,RepoName,disableRestart,BUILDOPTION,BUILDNUMBER,BUILDVERSION,
                           componentName,siteURL,siteName,userName,userPasswd,excluded_suites)
        
        result = autoTA.autoRun()