from django.shortcuts import get_object_or_404, render
from website.models import (Compartment, Protein, SignalMerged, SignalRaw,
                            Strain, Timepoint, Video,)


def protein_detail(request, common_name):
    """
    Page for each protein, with protein's videos, matrices, and other info.
    """
    # get protein from common name in url
    p = get_object_or_404(Protein, common_name=common_name)
    v = Video.objects.filter(protein_id=p.id)
    c = Compartment.objects.all()
    t = Timepoint.objects.all()
    num_timepoints = len(t)

    for video in v:
        # if summary length is longer than can fit on page, add truncated
        if len(video.summary) > 600:
            video.truncated_summary = video.summary[:500]

        # for unavailable videos, add a field so warning message displays
        if video.filename == "NUM1_PF1134_3_120510":
            video.lost = 1

        # get the worm strain depicted in the video
        video.strain = get_object_or_404(Strain, id=video.strain_id)

        """
        From the strain, generate genotype based on these 3 cases:
        1) if strain made by Miyeko, db genotype field is simply "pJon" or
           "pDESTMB16"
        2) if strain not made by Miyeko and on WormBase, the genotype field
           is empty
        3) if strain not made by Miyeko and NOT on Wormbase, full genotype
           listed in the genotype field
        """
        if video.strain.genotype == 'pJon':
            video.strain.genotype = (
                "unc-119(ed3) III; nnIs[unc-119(+) + Ppie-1::GFP-TEV-STag::" +
                p.common_name + "::3'pie-1]")
        elif video.strain.genotype == 'pDESTMB16':
            video.strain.genotype = (
                "unc-119(ed3) III; nnIs[unc-119(+) + Ppie-1::" +
                p.common_name + "::GFP::3'pie-1]")

        if not video.strain.genotype:
            video.strain.wormbase = (
                "http://www.wormbase.org/species/c_elegans/strain/" +
                video.strain.name)

        # process signals for the video; this relies on signals being sorted
        signals = SignalRaw.objects.filter(video_id=video.id)

        if signals:
            # list of rows for this matrix.
            # Each element: [compartment][list of signals for that row]
            matrix = []
            i = 0  # index for beginning of current row
            for compartment in c:  # for each row
                # add this row's compartment and signals
                matrix.append((compartment, signals[i:(i+num_timepoints)]))

                # raw matrices do have these rows, so skip them
                i += num_timepoints
            video.matrix = matrix

    # if consensus matrix (aka merge matrix), add to protein
    signals = SignalMerged.objects.filter(protein_id=p.id)
    if signals:
        consensus_matrix = []
        i = 0
        for compartment in c:  # for each row
            # add this row's compartment and signals
            consensus_matrix.append((compartment,
                                     signals[i:(i+num_timepoints)]))
            i += num_timepoints
        p.consensus_matrix = consensus_matrix

    # render page
    return render(request, 'protein_detail.html', {
        'protein': p,
        'videos': v,
        'timepoints': t,
    })
