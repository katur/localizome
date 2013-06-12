from django.template import RequestContext # extends Context; needed for STATIC_URL
from django.shortcuts import render_to_response, get_object_or_404 # r_to_r loads template, passes context, renders
from website.models import *

def protein_detail(request, common_name):
	"""
	Page for each protein, with protein's videos, matrices, and other information
	"""
	# get protein from common name in url
	p = get_object_or_404(Protein, common_name=common_name)
	v = Video.objects.filter(protein_id=p.id)
	c = Compartment.objects.all()
	t = Timepoint.objects.all()
	num_timepoints = len(t)

	matrices = [] # list of matrices. Each element: [video.id or "merge"][corresponding matrix]
	
	"""
	For each video, add and update various fields for the video,
	and add a matrix of signals to the list of matrices.
	"""
	for video in v:
		# if summary length is longer than can fit on page, add truncated summary
		if len(video.summary) > 600:
			video.truncated_summary = video.summary[:500]
		
		# for unavailable videos, add a field so warning message displays
		if video.filename == "NUM1_PF1134_3_120510":
			video.lost = 1
		
		# get the worm strain depicted in the video
		video.strain = get_object_or_404(Strain, id=video.strain_id)
		"""
		From the worm strain, generate genotype based on these 3 cases:
		1) if strain was made by Miyeko, the database's genotype field is simply "pJon" or "pDESTMB16",
			and the genotype can be derived from this along with the protein.
		2) if strain not made by Miyeko and is on WormBase, the genotype field is empty,
			and instead of listing genotype, add a link to WormBase
		3) if strain not made by Miyeko and is NOT on Wormbase, do nothing: the full genotype is already listed in the genotype field
		"""
		if video.strain.genotype == 'pJon': 
			video.strain.genotype = "unc-119(ed3) III; nnIs[unc-119(+) + Ppie-1::GFP-TEV-STag::" + p.common_name + "::3'pie-1]"
		elif video.strain.genotype == 'pDESTMB16':
			video.strain.genotype = "unc-119(ed3) III; nnIs[unc-119(+) + Ppie-1::" + p.common_name + "::GFP::3'pie-1]"
		
		if not video.strain.genotype:
			video.strain.wormbase = "http://www.wormbase.org/species/c_elegans/strain/" + video.strain.name
		
		# process signals for the video; this relies on signals being sorted
		signals = SignalRaw.objects.filter(video_id=video.id) # get all signals as one list
			
		matrix = [] # list of rows for this matrix. Each element: [compartment][list of signals for that row]
		i = 0 # index for beginning of current row
		if signals:
			for compartment in c: # for each row
				matrix.append((compartment, signals[i:(i+num_timepoints)])) # add this row's compartment and signals
				i += num_timepoints # raw matrices do have these rows, so skip them
			matrices.append((video, matrix))
	
	# add the merge matrix to matrices
	matrix = [] # refresh matrix
	i = 0 # refresh index
	signals = SignalMerged.objects.filter(protein_id=p.id) # get all signals as one list
	if signals:
		for compartment in c: # for each row
			matrix.append((compartment, signals[i:(i+num_timepoints)])) # add this row's compartment and signals
			i += num_timepoints
		matrices.append(("merge", matrix))
	
	# render page
	return render_to_response('protein_detail.html', {
		'protein':p, 
		'videos':v,
		'timepoints':t,
		'matrices':matrices,
	}, context_instance=RequestContext(request))
