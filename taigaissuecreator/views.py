from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from taigaissuecreator.forms import TaigaIssueForm
from taigaissuecreator.tasks import task_post_issue

# Create your views here.


@require_POST
@login_required
def post_issue(request):
    issue_form = TaigaIssueForm(request.POST)
    if issue_form.is_valid():
        files = request.FILES.getlist('attachments', None)
        task_post_issue.delay(
            posted_by=request.user,
            subject=issue_form.cleaned_data.get('subject'),
            description=issue_form.cleaned_data.get('description'),
            files=files
        )
        return HttpResponse(status=200)
    return HttpResponse(
        content=issue_form.errors.as_json(),
        status=500,
        content_type='application/json'
    )
