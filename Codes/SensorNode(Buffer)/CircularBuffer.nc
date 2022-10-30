interface CircularBuffer {

	async command int16_t firstElement();

	async command int16_t lastElement();

	async command uint16_t getWindow();

	command void putElem(int16_t put);

	command void putArray(int16_t *put, uint16_t size);

	command void setShift(uint16_t shiftV);

	async command uint16_t size();
       
}




