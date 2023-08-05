class Enum:   
    class ContentFilter: 
        """ 
        Content Filters

        Constants
        ---------
        OFF: MAY INCLUDED NSFW GIFS
        LOW: A LOWER RISK OF NSFW GIFS 
        MEDIUM: AN EVEN LOWER RISK OF NSFW GIFS 
        HIGH: THE LOWEST RISK OF NSFW GIFS
        """
        OFF = "off"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    class MediaFilter:
        """
        Media Filters

        Constants
        ---------
            Gifs
            ----
            GIF: HIGH QUALITY GIF FORMAT , LARGEST FORMAT OF GIF
            MEDIUMGIF: SMALL REDUCTION OF GIF FORMAT
            TINYGIF: REDUCED SIZE OF THE GIF FORMAT
            NANOGIF: SMALLEST SIZE OF GIF FORMAT
            
            Mp4
            ---
            MP4: HIGH QUALITY MP4 FORMAT , LARGEST FORMAT OF MP4
            LOOPEDMP4: SAME AS MP4
            TINYMP4: REDUCED SIZE OF THE MP4 FORMAT
            NANOMP4: SMALLEST SIZE OF MP4 FORMAT

            WEBM
            ----
            WEBM: LOWER QUALITY VIDEO FORMAT
            TINYWEBM: REDUCED SIZE OF WEBM FORMAT 
            NANOWEBM: SMALLEST SIZE OF WEBM FORMAT
        """ 
        GIF = "gif"
        MEDIUMGIF = "mediumgif"
        TINYGIF = "tinygif"
        NANOGIF = "nanogif"

        MP4 = "mp4"
        LOOPEDMP4 = "loopedmp4"
        TINYMP4 = "tinymp4"
        NANOMP4 = "nanomp4"

        WEBM = "webm"
        TINYWEBM = "tinywebm"
        NANOWEBM = "nanowebm"

    class LocaleMedia: 
        """
        Language Codes 

        Constants
        ---------
        ZH_CN: CHINESE
        ZH_TW: TAIWAN
        EN_US: ENGLISH 
        FR_FR: FRENCH
        DE_DE: GERMAN
        IT_IT: ITALIAN 
        JA_JP: JAPANESE
        KO_KR: KOREAN
        PT_BR: PORTUGUESE
        ES_ES: SPANISH
        """
        ZH_CN = "zh_CN"
        ZH_TW = "zh_TW"
        EN_US = "en_US"
        FR_FR = "fr_FR"
        DE_DE = "de_DE"
        IT_IT = "it_IT"
        JA_JP = "ja_JP"
        KO_KR = "ko_KR"
        PT_BR = "pt_BR"
        ES_ES = "es_ES"
