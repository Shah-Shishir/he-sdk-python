import settings


class InvalidParameterException(Exception):
    def __init__(self, message):
        super(InvalidParameterException, self).__init__(message)


class BaseAPIParameters(object):
    def __init__(self, client_secret, program_source, language):
        self.client_secret = client_secret
        self.source = program_source
        self.lang = language
        
        if not self.client_secret:
            raise InvalidParameterException(
            ("client_secret is needed. If you do",
            " not have a valid client_secret, please register your client at"
            " https://www.hackerearth.com/api/register")
            )

        if self.source is None:
            raise InvalidParameterException(
                "program_source is a mandatory parameter")

        if not self.lang:
            raise InvalidParameterException(
                "language parameter is mandatory")
        if not SupportedLanguages.is_lang_valid(self.lang):
            raise InvalidParameterException(
                ("{provided_language} is either not valid or not supported by "
                 "the API.").format(provided_language=self.lang)
                )

    def _build_params_dict(self):
        params = {
            'client_secret': self.client_secret,
            'source': self.source,
            'lang': self.lang
        }
        return params

    def get_params(self):
        params = self._build_params_dict()
        clean_params = self._clean_params(params)
        return clean_params

    def _clean_params(self, params):
        """Removes parameters whose values are set to None.
        """
        clean_params = {}
        for key, value in params.iteritems():
            if value is not None:
                clean_params[key] = value

        return clean_params




class CompileAPIParameters(object):
    def __init__(self, client_secret, source, language,
                async=0, 
                id=None,
                save=1,
                callback='',
                compressed=1
                ):
        super(CompileAPIParameters, self).__init__(client_secret,
            source, language)
        
        self.id = id
        self.save = save
        self.callback = callback
        self.compressed = compressed
        self.async = async

    def _build_params_dict(self):
        params = super(CompileAPIParameters, self)._build_params_dict()

        params.update({
            'id': self.id,
            'save': self.save,
            'callback': self.callback,
            'compressed': self.compressed,
            'async': self.async
            })
        return params


class RunAPIParameters(CompileAPIParameters):
    def __init__(self, client_secret, source, language,
                program_input=None,
                time_limit=settings.RUN_TIME_UPPER_LIMIT,
                memory_limit=settings.MEMORY_UPPER_LIMIT,
                async=0, 
                id=None,
                save=1,
                callback='',
                compressed=1,
                html=1,
                compiled=0
                ):
        super(RunAPIParameters, self).__init__(client_secret,
            source, language)
        
        self.id = id
        self.save = save
        self.callback = callback
        self.compressed = compressed
        self.async = async
        self.html = html
        self.compiled = compiled
        self.time_limit = min(time_limit, settings.RUN_TIME_UPPER_LIMIT)
        self.memory_limit = min(time_limit, settings.MEMORY_UPPER_LIMIT)

    def _build_params_dict(self):
        params = super(RunAPIParameters, self)._build_params_dict()

        params.update({
            'html': self.html,
            'compiled': self.compiled,
            'time_limit': self.time_limit,
            'memory_limit': self.memory_limit
            })
        return params


class SupportedLanguages(object):
    C = 'C'
    CPP = 'CPP'
    CPP11 = 'CPP11'
    CLOJURE = 'CLOJURE'
    CSHARP = 'CSHARP'
    JAVA = 'JAVA'
    JAVASCRIPT = 'JAVASCRIPT'
    HASKELL = 'HASKELL'
    PERL = 'PERL'
    PHP = 'PHP'
    PYTHON = 'PYTHON'
    RUBY = 'RUBY'

    @classmethod
    def is_lang_valid(cls, lang):
        """Checks whether the given language is supported
        by HackerEarth API.
        """
        if not lang in cls.__dict__:
            return False
        return True