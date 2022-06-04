from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError

class MyParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        content = super().parse(stream, media_type, parser_context)

        if stream.method == "POST":
            text = content.get("text")
            if not text:
                raise ParseError("this is a parse error")
            user_id = stream.user.id
            kwargs = parser_context.get("kwargs")
            post_id = kwargs.get("post_id")
            content_ = {
                "text": text,
                "user_id": user_id,
                "post_id": post_id,
            }
            return content_
        
        text = content.get("text")
        if not text:
            raise ParseError("this is a parse error")
        content_ = {
            "text": text
        }
        return content_
            
            
            


from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    
    if isinstance(exc, ParseError):
        response.data = {
            "error": "the error is parser error!!"
        }
        
    return response