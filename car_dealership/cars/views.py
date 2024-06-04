
import os
from .models import Manufacturer, BrandModel, Car, CarImages, Reservation
from .forms import EditCarForm, ManufacturerForm, BrandModelForm, CarForm, CarImagesForm, AddCarForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test


def superuser_required(view_func):
    decorated_view_func = login_required(
        user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func


def car_detail(request, car_id):
    # Fetch the car and its related images using prefetch_related for optimization
    car = get_object_or_404(
        Car.objects.prefetch_related('carimages_set'), id=car_id)
    car_images = car.carimages_set.all().order_by('-featured')
    # Get similar cars excluding the current car
    similar_cars = Car.objects.filter(model_name=car.model_name).exclude(
        id=car_id).prefetch_related('carimages_set')

    for similar_car in similar_cars:
        featured_image = similar_car.carimages_set.filter(
            featured=True).first()
        similar_car.featured_image = featured_image
    # Check if the user is authenticated and get the reservation if it exists
    user = request.user
    reservation = None
    if user.is_authenticated:
        reservation = Reservation.objects.filter(user=user, car=car).first()
    # Render the car detail template with the necessary context
    context = {'car': car, 'car_images': car_images,
               'similar_cars': similar_cars[:4], 'reservation': reservation}
    return render(request, 'car/car_detail.html', context)


def index(request):
    # Get filter and search parameters from the request
    brand_filter = request.GET.get('brand', None)
    model_filter = request.GET.get('model', None)
    fuel_filter = request.GET.get('fuel', None)
    year_filter = request.GET.get('year', None)
    min_price_filter = request.GET.get('minPrice', None)
    max_price_filter = request.GET.get('maxPrice', None)
    search_query = request.GET.get('search', None)
    # Build filters dictionary based on the parameters
    filters = {}
    if brand_filter:
        filters['model_name__manufacturer__name__iexact'] = brand_filter
    if model_filter:
        filters['model_name__name__iexact'] = model_filter
    if fuel_filter:
        filters['petrol_type'] = fuel_filter
    if year_filter:
        filters['year'] = year_filter
    if min_price_filter:
        filters['price__gte'] = min_price_filter
    if max_price_filter:
        filters['price__lte'] = max_price_filter
    # Filter cars based on the filters and search query
    cars = Car.objects.filter(
        **filters).prefetch_related('carimages_set')
    if search_query:
        cars = cars.filter(
            Q(model_name__name__icontains=search_query) |
            Q(model_name__manufacturer__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    # Order cars by creation date and paginate them
    cars = cars.order_by('-created_at')
    paginator = Paginator(cars, 10)
    page = request.GET.get('page', 1)
    try:
        cars_page = paginator.page(page)
    except PageNotAnInteger:
        cars_page = paginator.page(1)
    except EmptyPage:
        cars_page = paginator.page(paginator.num_pages)
    # Assign featured image to each car in the current page
    for car in cars_page:
        featured_image = car.carimages_set.filter(featured=True).first()
        car.featured_image = featured_image
    # Get unique brands and models for the filters
    unique_brands = Car.objects.values_list(
        'model_name__manufacturer__name', flat=True).distinct()
    models_list = []
    if brand_filter:
        models_list = Car.objects.filter(model_name__manufacturer__name=brand_filter).values_list(
            'model_name__name', flat=True).distinct()
    # Render the index template with the necessary context
    params = request.GET.copy()
    context = {'cars': cars_page, 'brands': unique_brands,
               'models': models_list, 'page_obj': cars_page, 'params': params}
    return render(request, 'index.html', context)


def get_additional_form_data(form, user):
    # Return additional data needed for forms based on the form type
    if form == 'manufacturer':
        return [i.name for i in Manufacturer.objects.all()], None
    
    if form == 'brandmodel':
        brandmodels = BrandModel.objects.all()
        manufacturers = Manufacturer.objects.all()
        return brandmodels, manufacturers
    return [], None


@superuser_required
def admin_forms(request, form_type):
    # Map form types to form classes and names
    form_map = {
        'manufacturer': ManufacturerForm,
        'brandmodel': BrandModelForm,
        'car': CarForm,
    }
    form_name_map = {
        'manufacturer': 'Manufacturer',
        'brandmodel': 'Brand Model',
        'car': 'Add Car',
    }
    # Get the form name and form class based on the form type provided
    form_name = form_name_map.get(form_type, 'Admin Form')
    form_class = form_map.get(form_type)
    user = request.user
    # If the form type is invalid, show an error message and redirect to index
    if not form_class:
        messages.error(request, 'Invalid form type.')
        return redirect('index')
    # Handle form submission
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            # Handle different form types separately
            if form_type == 'brandmodel':
                brand_model = form.save(commit=False)
                manufacturer = form.cleaned_data['manufacturer']
                brand_model.manufacturer = manufacturer
                brand_model.save()
                messages.success(request, 'Brand Model saved successfully.')
            else:
                form.save()
                messages.success(request, f'{form_name} saved successfully.')
            return redirect('admin_forms', form_type=form_type)
        else:
            messages.error(
                request, 'Form is not valid. Please check the fields.')
    else:
        # Create a new empty form if the request method is GET
        form = form_class()
    # Get additional data required for the form, if any
    data, manufacturers = get_additional_form_data(form_type, user)
    # Prepare the context for rendering the form template
    context = {'form': form, 'form_name': form_name, 'data': data}
    if manufacturers:
        context['manufacturers'] = manufacturers
    # Render the form template
    return render(request, 'forms/admin_forms.html', context)

@superuser_required
def edit_car(request, car_id):
    # Get the car object based on the provided car_id
    car = get_object_or_404(Car, id=car_id)
    # Handle form submission
    if request.method == 'POST':
        car_form = EditCarForm(request.POST, request.FILES, instance=car)

        if car_form.is_valid():
            # Save the car details
            car = car_form.save()
            has_featured_image = car.carimages_set.filter(
                featured=True).exists()
            # Handle uploaded images
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                if not has_featured_image and i == 0:
                    CarImages.objects.create(
                        car=car, image=image, featured=True)
                else:
                    CarImages.objects.create(
                        car=car, image=image)
            # Update the featured image if provided
            featured_image_id = request.POST.get('featured_image')
            if featured_image_id:
                # Unset previously featured images
                CarImages.objects.filter(
                    car=car, featured=False).update(featured=False)
                # Set new featured image
                featured_image = CarImages.objects.get(id=featured_image_id)
                featured_image.featured = True
                featured_image.save()

            messages.success(request, 'Car details updated successfully.')
            return redirect('car', car_id=car.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Create a form instance with the existing car details if the request method is GET
        car_form = EditCarForm(instance=car)
    # Get all images of the car
    car_images = car.carimages_set.all()
    # Prepare the context for rendering the form template
    context = {
        'car_form': car_form,
        'car_images': car_images,
        'car': car
    }
    # Render the edit car template
    return render(request, 'car/edit_car.html', context)


@superuser_required
def add_car(request):
    # Handle form submission
    if request.method == 'POST':
        form = AddCarForm(request.POST, request.FILES)

        if form.is_valid():
            brand_model_name = form.cleaned_data['brand_model_name']
            images = request.FILES.getlist('images')
            # Save the car details
            car = form.save(commit=False)
            car.model_name = brand_model_name
            car.save()

            # Handle uploaded images
            for i, image in enumerate(images):
                CarImages.objects.create(
                    car=car, image=image, featured=True if i == 0 else False)

            messages.success(request, 'Car added successfully.')
            return redirect('car', car_id=car.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Create a new empty form if the request method is GET
        form = AddCarForm()

    return render(request, 'car/add_car.html', {'form': form})


@superuser_required
def delete_car_image(request, image_id):
    # Get the image object based on the provided image_id
    image = get_object_or_404(CarImages, id=image_id)
    car = image.car
    car_id = car.id
    image_path = image.image.path

    if request.method == 'POST':
        featured = image.featured
        image.delete()
        # If the deleted image was featured, set another image as featured
        if featured:
            has_images = car.carimages_set.all()
            if len(has_images) > 0:
                has_images[0].featured = True
                has_images[0].save()
        # Delete the image file from the filesystem
        if os.path.isfile(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                messages.error(request, f'Error deleting image file: {e}')
                return redirect('edit_car', car_id=car_id)

        # Check if there are any remaining images for the car
        remaining_images = CarImages.objects.filter(car=car).exists()

        # If no images are left, remove the directory
        if not remaining_images:
            car_image_directory = os.path.dirname(image_path)
            try:
                os.rmdir(car_image_directory)
                messages.success(
                    request, 'Image and directory deleted successfully.')
            except Exception as e:
                messages.error(request, f'Error deleting directory: {e}')
        else:
            messages.success(request, 'Image deleted successfully.')

    return redirect('edit_car', car_id=car_id)


@login_required
def reserve_car(request, car_id):
    # Get the car object based on the provided car_id
    car = get_object_or_404(Car, id=car_id)
    # Handle form submission
    if request.method == 'POST':
        existing_reservation = Reservation.objects.filter(
            user=request.user, car=car).exists()
        if existing_reservation:
            messages.error(request, 'You have already reserved this car.')
        else:
            reservation = Reservation.objects.create(
                user=request.user, car=car)
            reservation.save()
            messages.success(request, 'Car reserved successfully!')

        return redirect('car', car_id=car.id)
    return redirect('car', car_id=car.id)


@login_required
def cancel_reservation(request, reservation_id):
    # Get the reservation object based on the provided reservation_id
    reservation = get_object_or_404(Reservation, id=reservation_id)
    # Handle form submission
    if request.method == 'POST':
        if reservation.user == request.user:
            reservation.delete()
            messages.success(request, 'Reservation cancelled successfully!')
        else:
            messages.error(
                request, 'You are not authorized to cancel this reservation.')
    # Redirect to the referring page
    return redirect(request.META.get('HTTP_REFERER', '/'))
