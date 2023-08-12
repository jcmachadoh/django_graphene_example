import graphene
from graphene_django import DjangoObjectType
from .models import Project, Task
from datetime import datetime


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description"
        )


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "done",
            "date",
            "project"
        )


class Query(graphene.ObjectType):
    projects = graphene.List(ProjectType)
    tasks = graphene.List(TaskType)
    project = graphene.Field(ProjectType, id=graphene.ID())
    task = graphene.Field(TaskType, id=graphene.ID())

    def resolve_projects(self, info):
        return Project.objects.all()

    def resolve_tasks(self, info):
        return Task.objects.all()

    def resolve_project(self, info, id):
        return Project.objects.get(id=id)

    def resolve_task(self, info, id):
        return Task.objects.get(pk=id)


class CreateProyectMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    project = graphene.Field(ProjectType)

    def mutate(self, info, name, description):
        project = Project(name=name, description=description)
        project.save()
        return CreateProyectMutation(project=project)


class CreateTaskMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        done = graphene.Boolean()
        # date = graphene.DateTime()
        project_id = graphene.ID(required=True)

    task = graphene.Field(TaskType)

    def mutate(self, info, title, description, done, project_id):
        project = Project.objects.get(pk=project_id)
        task = Task(title=title, description=description,
                    done=done, project=project)
        task.save()
        return CreateTaskMutation(task=task)


class DeleteProjectMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    project = graphene.Field(ProjectType)

    def mutate(self, info, id):
        project = Project.objects.get(id=id)
        project.delete()
        return DeleteProjectMutation(project=project)


class DeleteTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        task = Task.objects.get(id=id)
        task.delete()
        return DeleteTaskMutation(message="Task deleted")


class UpdateProjectMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()

    project = graphene.Field(ProjectType)

    def mutate(self, info, id, name, description):
        project = Project.objects.get(pk=id)
        project.name = name
        project.description = description
        project.save()
        return UpdateProjectMutation(project=project)


class UpdateTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        done = graphene.Boolean()
        project_id = graphene.ID()

    task = graphene.Field(TaskType)

    def mutate(self, info, id, title, description, done, project_id):
        project = Project.objects.get(pk=project_id)
        task = Task.objects.get(pk=id)
        task.title = title
        task.description = description
        task.done = done
        task.project = project
        task.date = datetime.now()
        task.save()
        return UpdateTaskMutation(task=task)


class ChangeStateTaskMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    task = graphene.Field(TaskType)

    def mutate(self, info, id):
        task = Task.objects.get(pk=id)
        if (task.done):
            task.done = False
        else:
            task.done = True
        task.save()
        return ChangeStateTaskMutation(task=task)


class Mutation(graphene.ObjectType):
    create_project = CreateProyectMutation.Field()
    create_task = CreateTaskMutation.Field()
    delete_project = DeleteProjectMutation.Field()
    delete_task = DeleteTaskMutation.Field()
    update_project = UpdateProjectMutation.Field()
    update_task = UpdateTaskMutation.Field()
    change_state_task = ChangeStateTaskMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
