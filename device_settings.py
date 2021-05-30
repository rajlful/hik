device_config = """<?xml version="1.0" encoding="UTF-8"?>
<StreamingChannel version="2.0" xmlns="http://www.hikvision.com/ver20/XMLSchema">
<id>101</id>
<channelName>IPdome</channelName>
<enabled>true</enabled>
    <Video>
        <enabled>true</enabled>
        <videoInputChannelID>1</videoInputChannelID>
        <videoCodecType>{}</videoCodecType>
        <videoScanType>progressive</videoScanType>
        <videoResolutionWidth>{}</videoResolutionWidth>
        <videoResolutionHeight>{}</videoResolutionHeight>
        <videoQualityControlType>VBR</videoQualityControlType>
        <fixedQuality>100</fixedQuality>
        <vbrUpperCap>4096</vbrUpperCap>
        <vbrLowerCap>32</vbrLowerCap>
        <maxFrameRate>{}]</maxFrameRate>
        <keyFrameInterval>800</keyFrameInterval>
        <snapShotImageType>JPEG</snapShotImageType>
        <H264Profile>Main</H264Profile>
        <GovLength>20</GovLength>
    </Video>
</StreamingChannel>"""