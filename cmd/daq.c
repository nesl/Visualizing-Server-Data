#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <comedilib.h>
#include <pthread.h> 
#include "config.h"

#define freq2periodns(F)	(int)(1e9/F)

#define RANGE10V	0
#define RANGE5V		1
#define RANGE2V		2
#define RANGE1V		3
#define RANGE500mV	4
#define RANGE200mV	5
#define RANGE100mV	6

#define RANGE		RANGE100mV

#define FREQUENCY	1000

#define N_CHANS		16

#define min(X,Y)	X < Y ? X : Y


static unsigned int chanlist[N_CHANS];

static comedi_range * range_info;
static lsampl_t maxdata;


#define SHAREDBUFSZ 4096
unsigned char sharedbuf[SHAREDBUFSZ];

comedi_cmd c;
comedi_t *dev;	


double channel_voltage[N_CHANS];
double channel_resistance[N_CHANS];


int prepare_channels() {
	int i;
	for(i = 0; i <  N_CHANS/2; i++){	
		chanlist[i] = CR_PACK(i, RANGE, AREF_DIFF);
	}
	for(i = N_CHANS/2; i <  N_CHANS; i++){	
		chanlist[i] = CR_PACK(i+N_CHANS/2, RANGE, AREF_DIFF);
	}	
	range_info = comedi_get_range(dev, 0, 0, RANGE);
	maxdata = comedi_get_maxdata(dev, 0, 0);
	
	
	
}

int prepare_cmd(comedi_cmd *cmd, int sampling_frequency) {
	memset(cmd,0,sizeof(*cmd));
	cmd->subdev =	0;
	cmd->flags = 0;
	cmd->start_src =	TRIG_NOW;
	cmd->start_arg =	0;
	cmd->scan_begin_src = TRIG_TIMER;
	/* Max frequency for PCI-6254 is 1MS/s, 1000 ns period */
	int scan_period = freq2periodns(sampling_frequency);
	cmd->scan_begin_arg = scan_period*N_CHANS;		/* in ns */
	/* Scan each channel sequentially */
	cmd->convert_src =	TRIG_TIMER;
	cmd->convert_arg =	scan_period;		
	/* Stop when all channels have completed */	
	cmd->scan_end_src =	TRIG_COUNT;
	cmd->scan_end_arg =	N_CHANS;		/* All the diff channels for PCI-6254 */
	/* Scan forever, until comedi_cancel() */	
	cmd->stop_src =		TRIG_NONE;
	cmd->stop_arg =		0;	
	/* Alternative trigger 
	cmd->stop_src =		TRIG_COUNT;
	cmd->stop_arg =		10;	
	*/
	cmd->chanlist =		chanlist;
	cmd->chanlist_len =	N_CHANS;	


}

int start_device() {

	int ret,i;	
	
	comedi_cmd *cmd=&c;
	
	dev = comedi_open("/dev/comedi0");
	if(!dev){
		comedi_perror("/dev/comedi0");
		exit(1);
	}	
	
	comedi_cancel(dev,0 );	
	
	prepare_channels();
	prepare_cmd(cmd, FREQUENCY);
	
	ret = comedi_command(dev, cmd);
	if(ret < 0){
		comedi_perror("comedi_command");
		exit(1);
	}
	//subdev_flags = comedi_get_subdevice_flags(dev, options.subdevice);	
	

	
}

void *process_sharedbuf(void *t) {
	int ret;
	int scan, channel;
	char strbuf[512];
	char *strbufptr;
	unsigned short * sharedbufptr = (unsigned short *)sharedbuf;
	for (scan = 0; scan < SHAREDBUFSZ/N_CHANS/2; scan++) {
		strbufptr=strbuf;
		for (channel = 0; channel < N_CHANS; channel++) {
			double physical_value = comedi_to_phys(*sharedbufptr, range_info, maxdata);
			physical_value = physical_value/channel_resistance[channel]*channel_voltage[channel];
			ret = sprintf(strbufptr,"%#+05.3f ",physical_value);
			sharedbufptr++;
			strbufptr+=ret;
		}
		printf("%s\b\n",strbuf);
	} 
	
}


void *read_device(void *t) {
	 
	int filenbr = comedi_fileno(dev);
	
	char buf[8192];
	char *bufptr;
	
	int i, ret;
	int total_data = 0;
	while (1) {
		ret = read(filenbr,buf,8192);
		bufptr = buf;
		int data_to_copy = ret;
		while (data_to_copy > 0) {
			int copy_now = min(SHAREDBUFSZ - total_data,data_to_copy);
			memcpy(sharedbuf+total_data,bufptr,copy_now);
			bufptr+=copy_now;
			data_to_copy-=copy_now;
			total_data+=copy_now;
			if (total_data == SHAREDBUFSZ) {
				total_data = 0;
				process_sharedbuf(NULL);
			}
		}
		

		
	}
	 
}

int main(int argc, char *argv[]) {
	
	int ret;
	pthread_t reader;
	
	if (argc < 2) {
		fprintf(stderr, "usage: %s daq0\n", argv[0]);
		exit(1);
	}
	
	load_config(argv[1], channel_resistance, channel_voltage);
	int i;
	for (i = 0; i < N_CHANS; i++) {
		fprintf(stderr, "channel: %d, res: %f, volt: %f\n", i, channel_resistance[i], channel_voltage[i]);
	}

	start_device();
		
	ret = pthread_create(&reader, NULL, read_device, NULL);

	pthread_join(reader, NULL);
	
	
}