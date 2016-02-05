from django.shortcuts import render
from website.models import Protein


def network(request):
    """
    Page with network image
    """
    p = Protein.objects.filter(network_x_coordinate__isnull=False)

    for protein in p:
        protein.network_x_coordinate_adjusted = protein.network_x_coordinate-30
        protein.network_y_coordinate_adjusted = protein.network_y_coordinate-5

    # render page
    return render(request, 'network.html', {'proteins': p})
