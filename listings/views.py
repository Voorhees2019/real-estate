from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from .choices import price_choices, bedroom_choices, state_choices


def listings(request):
    listings_list = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings_list, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    return render(request, 'listings/listings.html', {'listings': paged_listings})


def listing(request, listing_id):
    listing_obj = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'listings/listing.html', {'listing': listing_obj})


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET.get('keywords')
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    # City
        if 'city' in request.GET:
            city = request.GET.get('city')
            if city:
                queryset_list = queryset_list.filter(city__iexact=city)
    # State
        if 'state' in request.GET:
            state = request.GET.get('state')
            if state:
                queryset_list = queryset_list.filter(state__iexact=state)
    # Bedrooms
        if 'bedrooms' in request.GET:
            bedrooms = request.GET.get('bedrooms')
            if bedrooms:
                queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)
    # Price
        if 'price' in request.GET:
            price = request.GET.get('price')
            if price:
                queryset_list = queryset_list.filter(price__lte=price)

    return render(request, 'listings/search.html', {
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'listings': queryset_list,
        'values': request.GET
    })
