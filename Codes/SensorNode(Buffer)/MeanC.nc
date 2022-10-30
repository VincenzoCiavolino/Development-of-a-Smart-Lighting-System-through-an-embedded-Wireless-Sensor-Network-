configuration MeanC{

	provides interface ProcessingF;

}

implementation{

	components MeanP;
	ProcessingF = MeanP;

}
