from rest_framework.response import Response

class NSEMonitoringAPIResponse(Response):

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None,
                 schema=None):

        data = {
            'VERSION': 1,
            'schema': schema,
            'payload': data
        }

        super(NSEMonitoringAPIResponse, self).__init__(
            data, status, template_name, headers, exception, content_type
        )
