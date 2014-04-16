from fabric.api import lcd, local

def prepare_deployment():
    local('python manage.py test proj1')
    local('git add -p && git commit') # or local('hg add && hg commit')

def deploy():
    with lcd('/Users/7stud/django_projects/proj1/'):

        # With git...
        local('git pull /Users/7stud/dev_django_projects/proj1/')

        # With both
        local('python manage.py migrate myapp')
        local('python manage.py test myapp')
        local('python manage.py runserver')

