module MeanP{

	provides interface ProcessingF;

}

implementation {

	
	command int32_t ProcessingF.execute (int16_t *array, uint16_t length){
	int32_t mean=0;
	uint16_t i=0;
	for(i=0; i<length; i++){
		mean += *(array+1);}
	mean=mean/length;
	return mean;	
	}

}
