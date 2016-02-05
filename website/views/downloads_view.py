from django.shortcuts import get_object_or_404, render
from website.models import Protein, Video


def downloads(request):
    """
    Download page including downloads for a specific protein
    """
    proteins = Protein.objects.all()

    # render page
    return render(request, 'downloads.html', {'proteins': proteins})


def downloads_protein(request, common_name):
    proteins = Protein.objects.all()

    if common_name:
        p = get_object_or_404(Protein, common_name=common_name)
        v = Video.objects.filter(protein_id=p.id)

        for video in v:
            video.avi = video.filename + ".avi"
            video.mp4 = video.filename + ".mp4"
            video.ogv = video.filename + ".ogv"

    # render page
    return render(request, 'downloads.html', {
        'proteins': proteins,
        'protein': p,
        'videos': v,
    })
