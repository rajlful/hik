ipaddr='172.16.13.70'
user='admin' 
paswd='Admin321678' 
port=80

device_settings = """ 
<StreamingChannel>
<id>101</id>
<channelName>IPdome</channelName>
<enabled>true</enabled>
    <Video>
        <enabled>true</enabled>
        <videoInputChannelID>1</videoInputChannelID>
        <videoCodecType>H.264</videoCodecType>
        <videoScanType>progressive</videoScanType>
        <videoResolutionWidth>1</videoResolutionWidth>
        <videoResolutionHeight>1</videoResolutionHeight>
        <videoQualityControlType>VBR</videoQualityControlType>
        <fixedQuality>100</fixedQuality>
        <vbrUpperCap>4096</vbrUpperCap>
        <vbrLowerCap>32</vbrLowerCap>
        <maxFrameRate>2500</maxFrameRate>
        <keyFrameInterval>800</keyFrameInterval>
        <snapShotImageType>JPEG</snapShotImageType>
        <H264Profile>Main</H264Profile>
        <GovLength>20</GovLength>
    </Video>
</StreamingChannel>
"""

time_settings= '''<Time>
<timeMode>manual</timeMode>
<localTime>2021-06-03 16:06:12</localTime>
<timeZone>CST-3:00:00</timeZone>
</Time>'''

ntp_settings = '''<NTPServer>
<id>1</id>
<addressingFormatType>hostname</addressingFormatType>
<hostName>time.windows.com</hostName>
<portNo>123</portNo>
<synchronizeInterval>1440</synchronizeInterval>
</NTPServer>
'''