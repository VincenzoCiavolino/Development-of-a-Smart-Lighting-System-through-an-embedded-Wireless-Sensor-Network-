generic module CircularBufferC(uint16_t dim_buffer){
	provides interface Init;
	provides interface CircularBuffer;
}

implementation{
	int16_t buffer[dim_buffer];
	uint16_t shift = dim_buffer;
	int16_t win[dim_buffer];
	norace uint16_t i_bufferStart = 0;
	uint16_t i_curr = 0;

	norace uint8_t i;
       
	async command int16_t CircularBuffer.firstElement() {
		return buffer[i_bufferStart];
	}

	async command int16_t CircularBuffer.lastElement() {
		if (i_curr == 0)
			return buffer[dim_buffer - 1];
		else
			return buffer[(i_curr - 1)];
	}

	async command uint16_t CircularBuffer.getWindow() {
            
	atomic {
		for(i=0; i<dim_buffer; i++) {

			 win[i] = buffer[(i_bufferStart + i) % dim_buffer];
			//printf("win[%d]: %d \n", i,  win[i]);
		}
		i_bufferStart = (i_bufferStart + shift) % dim_buffer;
		return (uint16_t)&win[0];
		}
	}

	command void CircularBuffer.putElem(int16_t put) {
	    atomic {
		   buffer[i_curr] = (int16_t)put;
		   i_curr = (i_curr + 1) % dim_buffer;
	    }

	}

	command void CircularBuffer.putArray(int16_t *put, uint16_t size) {
		for(i=0; i<size; i++) {
			buffer[i_curr] = (int16_t)(*(put + i) );
			i_curr = (i_curr + 1) % dim_buffer;
		}
	}

	command void CircularBuffer.setShift(uint16_t shiftV) {
		shift = shiftV;
	}

	async command uint16_t CircularBuffer.size() {
		return dim_buffer;
	}

	command error_t Init.init() {
		memset(buffer, 0, sizeof(buffer));
		return SUCCESS;
	}

 }




