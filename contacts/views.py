from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from listings.models import Listing
from django.contrib import messages
from django.core.mail import send_mail
import os


def contact(request):
    if request.method == 'POST':
        listing_title = request.POST.get('listing_title')
        listing = Listing.objects.get(title=listing_title)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        realtor_email = request.POST.get('realtor_email')

        # Check if user has made an inquiry already
        if request.user.is_authenticated:
            has_contacted = Contact.objects.filter(listing=listing, user=request.user)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/' + str(listing.id))

        if request.user.is_authenticated:
            contact = Contact(listing=listing, user=request.user, name=name, email=email, phone=phone,
                              message=message)
        else:
            contact = Contact(listing=listing, name=name, email=email, phone=phone, message=message)
        contact.save()

        # Send email
        send_mail(
            'Property Listing Inquiry',
            'There has been an Inquiry for ' + listing.title + '. Sign into the admin panel for more info.',
            os.environ.get('EMAIL_USER'),
            [realtor_email, 'petrikartur@gmail.com'],
            fail_silently=False
        )
        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
    return redirect('/listings/' + str(listing.id))
