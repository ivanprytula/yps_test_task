from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class CSRFExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class JsonResponseMixin:
    def to_json_response(self, context, **resp_kwargs):
        return JsonResponse(self.get_context(context), **resp_kwargs)

    @staticmethod
    def get_context(context):
        """<Middle layer> method for context transformation."""
        return context
