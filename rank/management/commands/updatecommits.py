from django.core.management.base import BaseCommand, CommandError
import requests
from datetime import datetime
from rank.models import SourceCommit
from django.conf import settings
from datetime import timedelta


class Command(BaseCommand):
    help = 'Updates the commits from the Github server'

    def handle(self, *args, **options):
        def processCommits(queryDate):
            projectUrl = settings.GITLAB_SERVER + 'api/v4/projects'
            response = requests.get(projectUrl, headers={'PRIVATE_TOKEN': settings.GITLAB_PRIVATE_TOKEN})
            projects = response.json()
            for x in projects:
                queryId = str(x['id']);
                path_with_namespace = x['path_with_namespace']
                commitListUrl = settings.GITLAB_SERVER + 'api/v4/projects/' + queryId + '/repository/commits?since=' + queryDate
                response = requests.get(commitListUrl, headers={'PRIVATE_TOKEN': settings.GITLAB_PRIVATE_TOKEN})
                commits = response.json()
                for x in commits:
                    commitData = SourceCommit()
                    commitData.long_id = x['id']
                    commitData.short_id = x['short_id']
                    commitData.title = x['title']
                    commitData.message = x['message']
                    commitData.author_name = x['author_name']
                    commitData.author_login = x['author_email'].split('@', 1)[0]
                    commitData.author_email = x['author_email']
                    commitData.authored_date = x['authored_date']
                    commitData.committer_name = x['committer_name']
                    commitData.committer_email = x['committer_email']
                    commitData.committed_date = x['committed_date']
                    commitData.path_with_namespace = path_with_namespace
                    commitData.save()

        if settings.CODE_COMMIT_DISPLAY_ENABLED:
            try:
                lastCommit = SourceCommit.objects.values('committed_date').latest('committed_date')
                lastCommit = lastCommit['committed_date']
                processCommits(lastCommit)
            except (SourceCommit.DoesNotExist) as e:
                loadDate = (datetime.now() + timedelta(days=-settings.INITIAL_COMMIT_LOAD)).strftime(
                    "%Y-%m-%dT%H:%M:%S.000+00:00")
                processCommits(loadDate)