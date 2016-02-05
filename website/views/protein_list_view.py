from django.shortcuts import get_object_or_404, render
from website.models import Protein


def protein_list(request):
    """
    Page listing all proteins tested
    """
    # get all proteins
    p = Protein.objects.all().exclude(common_name="no GFP")
    c = get_object_or_404(Protein, common_name="no GFP")

    # render page
    return render(request, 'protein_list.html', {
        'proteins': p,
        'control': c,
    })
