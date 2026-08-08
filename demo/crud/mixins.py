from django.http import JsonResponse
from django.template.loader import render_to_string


class AjaxModalFormMixin:
    """Makes Create/Update views work inside a Bootstrap modal via fetch()."""
    modal_template_name = "crud/_modal_form.html"

    def is_ajax(self):
        return self.request.headers.get("x-requested-with") == "XMLHttpRequest"

    def render_to_response(self, context, **response_kwargs):
        if self.is_ajax():
            html = render_to_string(self.modal_template_name, context, request=self.request)
            return JsonResponse({"html": html})
        return super().render_to_response(context, **response_kwargs)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.is_ajax():
            html = render_to_string(
                self.modal_template_name, self.get_context_data(form=form), request=self.request
            )
            return JsonResponse({"success": False, "html": html}, status=400)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.is_ajax():
            return JsonResponse({"success": True})
        return response


class AjaxModalDeleteMixin:
    """Makes Delete views work inside a Bootstrap modal via fetch()."""
    modal_template_name = "crud/_modal_confirm_delete.html"

    def is_ajax(self):
        return self.request.headers.get("x-requested-with") == "XMLHttpRequest"

    def render_to_response(self, context, **response_kwargs):
        if self.is_ajax():
            html = render_to_string(self.modal_template_name, context, request=self.request)
            return JsonResponse({"html": html})
        return super().render_to_response(context, **response_kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.is_ajax():
            return JsonResponse({"success": True})
        return response