import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_get_course(api_client, course_factory):
    course = course_factory()

    url = reverse('courses-detail', args=[course.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


@pytest.mark.django_db
def test_get_courses_list(api_client, course_factory):
    courses = course_factory(_quantity=3)

    url = reverse('courses-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
    response_ids = {item['id'] for item in response.data}
    assert response_ids == {course.id for course in courses}


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    courses = course_factory(_quantity=3)
    target = courses[0]

    url = reverse('courses-list')
    response = api_client.get(url, data={'id': target.id})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == target.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course_factory(name='Python')
    course_factory(name='Django')
    target = course_factory(name='DRF')

    url = reverse('courses-list')
    response = api_client.get(url, data={'name': target.name})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == target.name


@pytest.mark.django_db
def test_create_course(api_client):
    url = reverse('courses-list')
    payload = {'name': 'New Course'}

    response = api_client.post(url, data=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == payload['name']


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory(name='Old Name')
    url = reverse('courses-detail', args=[course.id])
    payload = {'name': 'Updated Name'}

    response = api_client.patch(url, data=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == payload['name']


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
@pytest.mark.parametrize(
    'students_count, expected_status',
    [
        (2, status.HTTP_201_CREATED),
        (3, status.HTTP_400_BAD_REQUEST),
    ],
)
def test_max_students_per_course(
    api_client,
    student_factory,
    settings,
    students_count,
    expected_status,
):
    settings.MAX_STUDENTS_PER_COURSE = 2
    students = student_factory(_quantity=students_count)
    student_ids = [student.id for student in students]

    url = reverse('courses-list')
    response = api_client.post(
        url,
        data={'name': 'Limited Course', 'students': student_ids},
        format='json',
    )

    assert response.status_code == expected_status
