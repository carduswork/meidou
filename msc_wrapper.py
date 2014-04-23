#!/usr/bin/env python
#coding: utf-8

'''
讯飞云语音 windows SDK 的Python接口

基于讯飞云语音 windows SDK 1.046版，发布日期：2012-12-21

版本：1.0

作者：wangqyfm@foxmail.com
发布日期：2013-1-24

'''

import ctypes
import sys, wave, time, chardet

# 错误码
MSP_SUCCESS                                = 0
MSP_ERROR_FAIL                            = -1
MSP_ERROR_EXCEPTION                        = -2

# General errors 10100(0x2774) 
MSP_ERROR_GENERAL                        = 10100     # 0x2774 
MSP_ERROR_OUT_OF_MEMORY                    = 10101     # 0x2775 
MSP_ERROR_FILE_NOT_FOUND                = 10102     # 0x2776 
MSP_ERROR_NOT_SUPPORT                    = 10103     # 0x2777 
MSP_ERROR_NOT_IMPLEMENT                    = 10104     # 0x2778 
MSP_ERROR_ACCESS                        = 10105     # 0x2779 
MSP_ERROR_INVALID_PARA                    = 10106     # 0x277A 
MSP_ERROR_INVALID_PARA_VALUE            = 10107     # 0x277B 
MSP_ERROR_INVALID_HANDLE                = 10108     # 0x277C 
MSP_ERROR_INVALID_DATA                    = 10109     # 0x277D 
MSP_ERROR_NO_LICENSE                    = 10110     # 0x277E 
MSP_ERROR_NOT_INIT                        = 10111     # 0x277F 
MSP_ERROR_NULL_HANDLE                    = 10112     # 0x2780 
MSP_ERROR_OVERFLOW                        = 10113     # 0x2781 
MSP_ERROR_TIME_OUT                        = 10114     # 0x2782 
MSP_ERROR_OPEN_FILE                        = 10115     # 0x2783 
MSP_ERROR_NOT_FOUND                        = 10116     # 0x2784 
MSP_ERROR_NO_ENOUGH_BUFFER                = 10117     # 0x2785 
MSP_ERROR_NO_DATA                        = 10118     # 0x2786 
MSP_ERROR_NO_MORE_DATA                    = 10119     # 0x2787 
MSP_ERROR_NO_RESPONSE_DATA                = 10120     # 0x2788 
MSP_ERROR_ALREADY_EXIST                    = 10121     # 0x2789 
MSP_ERROR_LOAD_MODULE                    = 10122     # 0x278A 
MSP_ERROR_BUSY                            = 10123     # 0x278B 
MSP_ERROR_INVALID_CONFIG                = 10124     # 0x278C 
MSP_ERROR_VERSION_CHECK                 = 10125     # 0x278D 
MSP_ERROR_CANCELED                        = 10126     # 0x278E 
MSP_ERROR_INVALID_MEDIA_TYPE            = 10127     # 0x278F 
MSP_ERROR_CONFIG_INITIALIZE                = 10128     # 0x2790 
MSP_ERROR_CREATE_HANDLE                    = 10129     # 0x2791 
MSP_ERROR_CODING_LIB_NOT_LOAD            = 10130     # 0x2792 

# Error codes of network 10200(0x27D8)
MSP_ERROR_NET_GENERAL                    = 10200     # 0x27D8 
MSP_ERROR_NET_OPENSOCK                     = 10201     # 0x27D9    # Open socket 
MSP_ERROR_NET_CONNECTSOCK                  = 10202     # 0x27DA    # Connect socket 
MSP_ERROR_NET_ACCEPTSOCK                   = 10203     # 0x27DB    # Accept socket 
MSP_ERROR_NET_SENDSOCK                     = 10204     # 0x27DC    # Send socket data 
MSP_ERROR_NET_RECVSOCK                     = 10205     # 0x27DD    # Recv socket data 
MSP_ERROR_NET_INVALIDSOCK                  = 10206     # 0x27DE    # Invalid socket handle 
MSP_ERROR_NET_BADADDRESS                   = 10207     # 0x27EF    # Bad network address 
MSP_ERROR_NET_BINDSEQUENCE                 = 10208     # 0x27E0    # Bind after listen/connect 
MSP_ERROR_NET_NOTOPENSOCK                  = 10209     # 0x27E1    # Socket is not opened 
MSP_ERROR_NET_NOTBIND                     = 10210     # 0x27E2    # Socket is not bind to an address 
MSP_ERROR_NET_NOTLISTEN                    = 10211     # 0x27E3    # Socket is not listening 
MSP_ERROR_NET_CONNECTCLOSE                 = 10212     # 0x27E4    # The other side of connection is closed 
MSP_ERROR_NET_NOTDGRAMSOCK                 = 10213     # 0x27E5    # The socket is not datagram type 
MSP_ERROR_NET_DNS                         = 10214     # 0x27E6    # domain name is invalid or dns server does not function well 

# Error codes of mssp message 10300(0x283C) 
MSP_ERROR_MSG_GENERAL                    = 10300     # 0x283C 
MSP_ERROR_MSG_PARSE_ERROR                = 10301     # 0x283D 
MSP_ERROR_MSG_BUILD_ERROR                = 10302     # 0x283E 
MSP_ERROR_MSG_PARAM_ERROR                = 10303     # 0x283F 
MSP_ERROR_MSG_CONTENT_EMPTY                = 10304     # 0x2840 
MSP_ERROR_MSG_INVALID_CONTENT_TYPE        = 10305     # 0x2841 
MSP_ERROR_MSG_INVALID_CONTENT_LENGTH    = 10306     # 0x2842 
MSP_ERROR_MSG_INVALID_CONTENT_ENCODE    = 10307     # 0x2843 
MSP_ERROR_MSG_INVALID_KEY                = 10308     # 0x2844 
MSP_ERROR_MSG_KEY_EMPTY                    = 10309     # 0x2845 
MSP_ERROR_MSG_SESSION_ID_EMPTY            = 10310     # 0x2846 
MSP_ERROR_MSG_LOGIN_ID_EMPTY            = 10311     # 0x2847 
MSP_ERROR_MSG_SYNC_ID_EMPTY                = 10312     # 0x2848 
MSP_ERROR_MSG_APP_ID_EMPTY                = 10313     # 0x2849 
MSP_ERROR_MSG_EXTERN_ID_EMPTY            = 10314     # 0x284A 
MSP_ERROR_MSG_INVALID_CMD                = 10315     # 0x284B 
MSP_ERROR_MSG_INVALID_SUBJECT            = 10316     # 0x284C 
MSP_ERROR_MSG_INVALID_VERSION            = 10317     # 0x284D 
MSP_ERROR_MSG_NO_CMD                    = 10318     # 0x284E 
MSP_ERROR_MSG_NO_SUBJECT                = 10319     # 0x284F 
MSP_ERROR_MSG_NO_VERSION                = 10320     # 0x2850 
MSP_ERROR_MSG_MSSP_EMPTY                = 10321     # 0x2851 
MSP_ERROR_MSG_NEW_RESPONSE                = 10322     # 0x2852 
MSP_ERROR_MSG_NEW_CONTENT                = 10323     # 0x2853 
MSP_ERROR_MSG_INVALID_SESSION_ID        = 10324     # 0x2854 

# Error codes of DataBase 10400(0x28A0)
MSP_ERROR_DB_GENERAL                    = 10400     # 0x28A0 
MSP_ERROR_DB_EXCEPTION                    = 10401     # 0x28A1 
MSP_ERROR_DB_NO_RESULT                    = 10402     # 0x28A2 
MSP_ERROR_DB_INVALID_USER                = 10403     # 0x28A3 
MSP_ERROR_DB_INVALID_PWD                = 10404     # 0x28A4 
MSP_ERROR_DB_CONNECT                    = 10405     # 0x28A5 
MSP_ERROR_DB_INVALID_SQL                = 10406     # 0x28A6 
MSP_ERROR_DB_INVALID_APPID                = 10407    # 0x28A7 

# Error codes of Resource 10500(0x2904)
MSP_ERROR_RES_GENERAL                    = 10500     # 0x2904 
MSP_ERROR_RES_LOAD                      = 10501     # 0x2905    # Load resource 
MSP_ERROR_RES_FREE                      = 10502     # 0x2906    # Free resource 
MSP_ERROR_RES_MISSING                   = 10503     # 0x2907    # Resource File Missing 
MSP_ERROR_RES_INVALID_NAME              = 10504     # 0x2908    # Invalid resource file name 
MSP_ERROR_RES_INVALID_ID                = 10505     # 0x2909    # Invalid resource ID 
MSP_ERROR_RES_INVALID_IMG               = 10506     # 0x290A    # Invalid resource image pointer 
MSP_ERROR_RES_WRITE                     = 10507     # 0x290B    # Write read-only resource 
MSP_ERROR_RES_LEAK                      = 10508     # 0x290C    # Resource leak out 
MSP_ERROR_RES_HEAD                      = 10509     # 0x290D    # Resource head currupt 
MSP_ERROR_RES_DATA                      = 10510     # 0x290E    # Resource data currupt 
MSP_ERROR_RES_SKIP                      = 10511     # 0x290F    # Resource file skipped 

# Error codes of TTS 10600(0x2968)
MSP_ERROR_TTS_GENERAL                    = 10600     # 0x2968 
MSP_ERROR_TTS_TEXTEND                      = 10601     # 0x2969   # Meet text end 
MSP_ERROR_TTS_TEXT_EMPTY                = 10602     # 0x296A   # no synth text 

# Error codes of Recognizer 10700(0x29CC) 
MSP_ERROR_REC_GENERAL                    = 10700     # 0x29CC 
MSP_ERROR_REC_INACTIVE                    = 10701     # 0x29CD 
MSP_ERROR_REC_GRAMMAR_ERROR                = 10702     # 0x29CE 
MSP_ERROR_REC_NO_ACTIVE_GRAMMARS        = 10703     # 0x29CF 
MSP_ERROR_REC_DUPLICATE_GRAMMAR            = 10704     # 0x29D0 
MSP_ERROR_REC_INVALID_MEDIA_TYPE        = 10705     # 0x29D1 
MSP_ERROR_REC_INVALID_LANGUAGE            = 10706     # 0x29D2 
MSP_ERROR_REC_URI_NOT_FOUND                = 10707     # 0x29D3 
MSP_ERROR_REC_URI_TIMEOUT                = 10708     # 0x29D4 
MSP_ERROR_REC_URI_FETCH_ERROR            = 10709     # 0x29D5 

# Error codes of Speech Detector 10800(0x2A30) 
MSP_ERROR_EP_GENERAL                    = 10800     # 0x2A30 
MSP_ERROR_EP_NO_SESSION_NAME            = 10801     # 0x2A31 
MSP_ERROR_EP_INACTIVE                   = 10802     # 0x2A32 
MSP_ERROR_EP_INITIALIZED                = 10803     # 0x2A33 

# Error codes of TUV   
MSP_ERROR_TUV_GENERAL                    = 10900     # 0x2A94 
MSP_ERROR_TUV_GETHIDPARAM                = 10901     # 0x2A95    # Get Busin Param huanid
MSP_ERROR_TUV_TOKEN                      = 10902     # 0x2A96    # Get Token 
MSP_ERROR_TUV_CFGFILE                    = 10903     # 0x2A97    # Open cfg file  
MSP_ERROR_TUV_RECV_CONTENT              = 10904     # 0x2A98    # received content is error 
MSP_ERROR_TUV_VERFAIL                      = 10905     # 0x2A99    # Verify failure 

# Error codes of IMTV 
MSP_ERROR_LOGIN_SUCCESS                    = 11000     # 0x2AF8    # 成功 
MSP_ERROR_LOGIN_NO_LICENSE                = 11001     # 0x2AF9    # 试用次数结束，用户需要付费 
MSP_ERROR_LOGIN_SESSIONID_INVALID        = 11002     # 0x2AFA    # SessionId失效，需要重新登录通行证  
MSP_ERROR_LOGIN_SESSIONID_ERROR            = 11003     # 0x2AFB    # SessionId为空，或者非法 
MSP_ERROR_LOGIN_UNLOGIN                      = 11004     # 0x2AFC    # 未登录通行证 
MSP_ERROR_LOGIN_INVALID_USER              = 11005     # 0x2AFD    # 用户ID无效 
MSP_ERROR_LOGIN_INVALID_PWD                  = 11006     # 0x2AFE    # 用户密码无效 
MSP_ERROR_LOGIN_SYSTEM_ERROR            = 11099     # 0x2B5B    # 系统错误 

# Error codes of HCR 
MSP_ERROR_HCR_GENERAL                    = 11100
MSP_ERROR_HCR_RESOURCE_NOT_EXIST        = 11101
MSP_ERROR_HCR_CREATE                    = 11102
MSP_ERROR_HCR_DESTROY                    = 11103
MSP_ERROR_HCR_START                        = 11104
MSP_ERROR_HCR_APPEND_STROKES            = 11105
MSP_ERROR_HCR_GET_RESULT                = 11106
MSP_ERROR_HCR_SET_PREDICT_DATA            = 11107
MSP_ERROR_HCR_GET_PREDICT_RESULT        = 11108

# Error codes of http 12000(0x2EE0) 
MSP_ERROR_HTTP_BASE                        = 12000    # 0x2EE0 

# 采样类型定义
MSP_AUDIO_SAMPLE_INIT           = 0x00
MSP_AUDIO_SAMPLE_FIRST          = 0x01
MSP_AUDIO_SAMPLE_CONTINUE       = 0x02
MSP_AUDIO_SAMPLE_LAST           = 0x04

# 录音状态定义
MSP_REC_STATUS_SUCCESS              = 0
MSP_REC_STATUS_NO_MATCH             = 1
MSP_REC_STATUS_INCOMPLETE           = 2
MSP_REC_STATUS_NON_SPEECH_DETECTED  = 3
MSP_REC_STATUS_SPEECH_DETECTED      = 4
MSP_REC_STATUS_COMPLETE             = 5
MSP_REC_STATUS_MAX_CPU_TIME         = 6
MSP_REC_STATUS_MAX_SPEECH           = 7
MSP_REC_STATUS_STOPPED              = 8
MSP_REC_STATUS_REJECTED             = 9
MSP_REC_STATUS_NO_SPEECH_FOUND      = 10
MSP_REC_STATUS_FAILURE = MSP_REC_STATUS_NO_MATCH

# 端点检测状态定义
MSP_EP_LOOKING_FOR_SPEECH   = 0
MSP_EP_IN_SPEECH            = 1
MSP_EP_AFTER_SPEECH         = 3
MSP_EP_TIMEOUT              = 4
MSP_EP_ERROR                = 5
MSP_EP_MAX_SPEECH           = 6
MSP_EP_IDLE                 = 7  # internal state after stop and before start

# 同步处理标记
MSP_TTS_FLAG_STILL_HAVE_DATA        = 1
MSP_TTS_FLAG_DATA_END               = 2
MSP_TTS_FLAG_CMD_CANCELED           = 4

# 导入dll
msp_dll = ctypes.windll.LoadLibrary('msc.dll')

def mspQISRInit(configs):
    ''' 初始化MSC的ISR部分，返回错误代码
    函数原型 int MSPAPI QISRInit(const char* configs);
    '''
    return msp_dll.QISRInit(configs)

def mspQISRSessionBegin(grammarList, params):
    ''' 开始一个ISR会话，返回会话ID
    函数原型 const char* MSPAPI QISRSessionBegin(const char* grammarList,
                                             const char* params, 
                                             int *errorCode);
    '''
    sessionBg = msp_dll.QISRSessionBegin
    sessionBg.restype = ctypes.c_char_p
    errorCode = ctypes.c_int(0)

    result = sessionBg(grammarList, params, ctypes.byref(errorCode))

    return errorCode.value, result

def mspQISRGrammarActivate(sessionID, grammar, type, weight):
    ''' 激活一个指定的语法，返回错误代码
    函数原型 int MSPAPI QISRGrammarActivate(const char* sessionID, 
                                            const char* grammar, 
                                            const char* type, int weight);
    '''

    return msp_dll.QISRGrammarActivate(sessionID, grammar, type, weight)

def mspQISRAudioWrite(sessionID, waveData, audioStatus):
    ''' 写入用来识别的语音，返回错误代码
    函数原型 int MSPAPI QISRAudioWrite(const char* sessionID, 
                                       const void* waveData, 
                                       unsigned int waveLen, 
                                       int audioStatus, 
                                       int* epStatus, 
                                       int* recogStatus);
    '''

    epStatus = ctypes.c_int(0)
    recogStatus = ctypes.c_int(0)

    result = msp_dll.QISRAudioWrite(sessionID, \
                                    waveData, len(waveData), \
                                    audioStatus, \
                                    ctypes.byref(epStatus), \
                                    ctypes.byref(recogStatus))

    return result, epStatus.value, recogStatus.value

def mspQISRGetResult(sessionID, waitTime):
    ''' 获取识别结果
    函数原型 const char * MSPAPI QISRGetResult(const char* sessionID, 
                                               int* rsltStatus, 
                                               int waitTime, 
                                               int *errorCode);
    '''

    rsltStatus = ctypes.c_int(0)
    errorCode = ctypes.c_int(0)
    
    getResult = msp_dll.QISRGetResult
    getResult.restype = ctypes.c_char_p

    result = getResult(sessionID, ctypes.byref(rsltStatus), \
                       waitTime, ctypes.byref(errorCode))

    return errorCode.value, rsltStatus.value, result

def mspQISRSessionEnd(sessionID, hints):
    ''' 结束一路会话，返回错误代码
    函数原型 int MSPAPI QISRSessionEnd(const char* sessionID, const char* hints)
    '''
    return msp_dll.QISRSessionEnd(sessionID, hints)

def mspQISRGetParam(sessionID, paramName):
    ''' 获取与识别交互相关的参数，返回错误代码
    函数原型 int MSPAPI QISRGetParam(const char* sessionID, 
                                     const char* paramName, 
                                     char* paramValue, 
                                     unsigned int* valueLen)
    '''
    paramValue  = ctypes. create_string_buffer(1024) # 这里可能会错～
    valueLen = ctypes.c_uint()

    result = msp_dll.QISRGetParam(sessionID, \
                                  paramName, \
                                  paramValue, \
                                  ctypes.byref(valueLen))
    return result, paramValue.value

def mspQISRFini():
    ''' 逆初始化MSC的ISR部分 
    函数原型 int MSPAPI QISRFini(void);
    '''
    return msp_dll.QISRFini()


def sendwav(filenme):
    param = "rst=plain,sub=iat,ssm=1,auf=audio/L16;rate=16000,aue=speex,ent=sms16k"
    err, sess_id = mspQISRSessionBegin(None, param)
    if err != MSP_SUCCESS:
        print u'不能开始session.[%d]' % err
    try:
        # 读取wav文件
        f=wave.open(filenme, 'rb')
        n=f.getnframes() 
        frames=f.readframes(n)
        f.close

        # 发送语音数据
        err, ep, rec = mspQISRAudioWrite(sess_id, frames, MSP_AUDIO_SAMPLE_LAST)
        if err != MSP_SUCCESS:
            print u'发送语音数据失败.[%d]' % err
            return u'发送语音数据失败.[%d]' % err
        else:
            print u'发送成功，端点检测状态：[%d]，识别器状态：[%d].' % (ep, rec)

            complete = False
            # 取回结果
            times = 3
            while not complete:
                err, state, result = mspQISRGetResult(sess_id, 0)
                if err != MSP_SUCCESS:
                    print u'不能取回结果.[%d]' % err
                else:
                    complete = True
                    if state == MSP_REC_STATUS_SUCCESS:
                        print u'识别成功'
                    elif state == MSP_REC_STATUS_NO_MATCH:
                        print u'识别结束，没有识别结果'
                    elif state == MSP_REC_STATUS_INCOMPLETE:
                        complete = False
                        print u'正在识别中'
                    elif state == MSP_REC_STATUS_SPEECH_DETECTED:
                        print u'发现有效音频'
                    elif state == MSP_REC_STATUS_COMPLETE:
                        pass
                        #print u'识别结束'
                    elif state == MSP_REC_STATUS_NO_SPEECH_FOUND:
                        print u'没有发现音频'
                    else:
                        print u'其他状态：%d.' % state

                times = times - 1
                if not times:break
                
                if not complete:time.sleep(.5)
                else:break
        
            endSession(sess_id)
            print u'结果：', result
            if result:return result.decode('gb2312').encode('utf-8')
            else:return None
    except Exception as e:
        print u'发生错误：', e

def endSession(sid):
    ''' 结束会话
    成功返回True，否则返回False
    '''
    retval = mspQISRSessionEnd(sid, None)
    if retval != MSP_SUCCESS:
        print u'结束会话时发生错误.[%d]' % retval
        return False
    return True

def regStart():
    configs="appid=53074c90"#50ffa670"#51bc701f"
    retval = mspQISRInit(configs)
    if retval != MSP_SUCCESS:
        print u'初始化错误.[%d]' % retval
        #sys.exit()

def regEnd():
    retval = mspQISRFini()
    if retval != MSP_SUCCESS:
        print u'逆初始化错误.[%d]' % retval
    print 'End'

        
if __name__ == '__main__':
    regStart()
    #sendwav(r'wav\2014-04-09_20_14_48.wav')
    sendwav('wav_test.wav')
    regEnd()
