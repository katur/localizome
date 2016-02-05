from django.shortcuts import render
from django.db.models import Q
from website.models import Compartment, Timepoint, SignalMerged


def spatiotemporal_search(request):
    """
    Page with spatiotemporal matrix showing number of proteins
    expressed at every spatiotemporal point
    """
    # get all compartments and timepoints
    c = Compartment.objects.all()
    t = Timepoint.objects.all()

    # create a 2D array of all 0s for the matrix signals
    signal_matrix = [[0 for x in range(0, len(t)+1)]
                     for x in range(0, len(c)+1)]

    # get ALL merge signals
    signals = SignalMerged.objects.filter(Q(strength=2) | Q(strength=3))

    # iterate through signals, incrementing corresponding cell in matrix
    for signal in signals:
        signal_matrix[signal.compartment_id][signal.timepoint_id] += 1

    # list of rows for this matrix.
    # Each element: [compartment][list of signals for that row]
    matrix = []

    for compartment in c:
        matrix.append((compartment, signal_matrix[compartment.id][1:]))

    # render page
    return render(request, 'spatiotemporal_search.html', {
        'timepoints': t,
        'spatiotemporal_matrix': matrix,
    })


def spatiotemporal_both(request, compartment, timepoint):
    """
    Results page for coexpressed proteins given a compartment AND timepoint
    """
    # get this timepoint and compartment
    c = Compartment.objects.get(id=compartment)
    t = Timepoint.objects.get(id=timepoint)

    # get all proteins present or weak in this compartment at this timepoint
    s = SignalMerged.objects.filter(
        Q(compartment_id=compartment),
        Q(timepoint_id=timepoint),
        Q(strength=2) | Q(strength=3)
    )

    # render page
    return render(request, 'spatiotemporal_results.html', {
        'signals': s,
        'compartment': c,
        'timepoint': t
    })


def spatiotemporal_compartment(request, compartment):
    """
    Results page for coexpressed proteins given a compartment only
    """
    # get this compartment and ALL timepoints
    c = Compartment.objects.get(id=compartment)
    t = Timepoint.objects.all()

    # get all proteins present or weak at any time in this compartment
    p = SignalMerged.objects.values('protein').filter(
        Q(compartment_id=compartment),
        Q(strength=2) | Q(strength=3)
    ).distinct()

    # get ALL signals for these proteins in this compartments
    s = SignalMerged.objects.filter(
        Q(protein_id__in=p),
        Q(compartment_id=compartment)
    )

    # render page
    return render(request, 'spatiotemporal_results.html', {
        'signals': s,
        'compartment': c,
        'timepoints': t
    })


def spatiotemporal_timepoint(request, timepoint):
    """
    Results page for coexpressed proteins given a timepoint only
    """
    # get this timepoint and ALL compartments
    t = Timepoint.objects.get(id=timepoint)
    c = Compartment.objects.all()

    # get all proteins present or weak in any compartment at this timepoint
    p = SignalMerged.objects.values('protein').filter(
        Q(timepoint_id=timepoint),
        Q(strength=2) | Q(strength=3)
    ).distinct()

    # get ALL signals for these proteins at this timepoint
    s = SignalMerged.objects.filter(
        Q(protein__in=p),
        Q(timepoint_id=timepoint)
    )

    # render page
    return render(request, 'spatiotemporal_results.html', {
        'signals': s,
        'timepoint': t,
        'compartments': c
    })
