import graphene
from graphene_django import DjangoObjectType
from .models import *
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id # mengambil id untuk

# mengambil dari database dan dibuat meta
 
class CityNode(DjangoObjectType):
    class Meta:
        model = City
        filter_fields = ['city_name']
        interfaces = (graphene.relay.Node,)

class TitleNode(DjangoObjectType):
    class Meta:
        model = Title
        filter_fields = ['title_name']
        interfaces = (graphene.relay.Node,)

class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee
        # filter digunakan untuk mengambil coloumn
        filter_fields = [
            'employee_name',
            'employee_city__city_name',
            'employee_title__title_name'
        ]
        interfaces = (graphene.relay.Node,)
        
# membuat query pemanggilan
class Query(object):
    city = graphene.relay.Node.Field(CityNode)
    all_cities = DjangoFilterConnectionField(CityNode)
    
    title = graphene.relay.Node.Field(TitleNode)
    all_titles = DjangoFilterConnectionField(TitleNode)
    
    employee = graphene.relay.Node.Field(EmployeeNode)
    all_employees = DjangoFilterConnectionField(EmployeeNode)

# menambah title di api
class CreateTitle(graphene.relay.ClientIDMutation):
    title = graphene.Field(TitleNode)

    class Input:
        title_name = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        title = Title(
            title_name=input.get('title_name')
        )
        title.save()
        return CreateTitle(title=title)

class CreateCity(graphene.relay.ClientIDMutation):
    city = graphene.Field(CityNode)

    class Input:
        city_name = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        city = City(
            city_name=input.get('city_name')
        )
        city.save()
        return CreateCity(city=city)


class CreateEmployee(graphene.relay.ClientIDMutation):
    employee = graphene.Field(EmployeeNode) #Field bertujuan unuk mengambil isi dari database

    class Input:
        employee_name   = graphene.String()
        employee_city   = graphene.String()
        employee_title  = graphene.String()

    def mutate_and_get_payload(root,info,**input):
        employee = Employee(
            employee_name = input.get('employee_name'),
            employee_city = City.objects.get(
                city_name = input.get('employee_city')
            ),
            employee_title = Title.objects.get(
                title_name = input.get('employee_title')
            )
        )
        employee.save()
        return CreateEmployee(employee=employee)


# mengaupdate API
class UpdateEmployee(graphene.relay.ClientIDMutation):
    employee = graphene.Field(EmployeeNode)

    class Input:
        id = graphene.String()
        employee_name = graphene.String()
        employee_city = graphene.String()
        employee_title = graphene.String()

    def mutate_and_get_payload(root,info,**input):
        employee = Employee.objects.get(
            pk=from_global_id(input.get('id'))[1]
        )
        employee.employee_name = input.get('employee_name')
        # hanya mengedit nama saja , karna yang lain manggil forign key 
        # employee.employee_city = City.objects.get(
        #     city_name = input.get('employee_city')
        # )
        # employee.employee_title =Title.objects.get(
        #     title_name = input.get('employee_title')
        # )
        employee.save()
        return UpdateEmployee(employee=employee)


# delete data    
class DeleteEmployee(graphene.relay.ClientIDMutation):
    employee = graphene.Field(EmployeeNode)

    class Input:
        id = graphene.String()

    def mutate_and_get_payload(root,info,**input):
         employee = Employee.objects.get(
             pk=from_global_id(input.get('id'))[1]
         )
         employee.delete()
         return DeleteEmployee(employee=employee)

# bertujuan untuk meregister di grapql
class Mutation(graphene.AbstractType):
    
    # ADD data POST
    create_title = CreateTitle.Field() # ini nama yg di panggil di grapiql
    create_city = CreateCity.Field()
    create_employee = CreateEmployee.Field()

    # Update data / PUT
    update_employee = UpdateEmployee.Field()

    # Deleting data
    delete_employee = DeleteEmployee.Field()