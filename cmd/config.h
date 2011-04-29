/*
 *  config.h
 *  
 *
 *  Created by Lucas Wanner on 2/3/11.
 *  Copyright 2011 UCLA. All rights reserved.
 *
 */

#ifndef CHANNEL_CONFIG
#define CHANNEL_CONFIG



#define ABS_PATH "/home/nesl/Visualizing-Server-Data/"
#define FILE_PREFIX "cmd/config/"
#define RES_SRT		"_resistance"
#define VOL_SRT		"_voltage"

int load_one(char * daqname, char * resource, double * dest) {
	char filename[256];
	memset(filename,0,256);
	float values[16];	
	FILE * fd;
    strcat(filename, ABS_PATH);
	strcat(filename,FILE_PREFIX);
	strcat(filename,daqname);
	strcat(filename,resource);
	fd = fopen(filename,"r");
	
	fscanf(fd, "%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",
		   &values[0],&values[1],&values[2],&values[3],&values[4],&values[5],&values[6],&values[7],
		   &values[8],&values[9],&values[10],&values[11],&values[12],&values[13],&values[14],&values[15]);
	int i;
	for (i = 0; i<16; i++) {
		dest[i] = values[i];
	}
}


int load_config(char * daqname, double *res, double *volt) {

	
	
	load_one(daqname,RES_SRT,res);
	load_one(daqname,VOL_SRT,volt);
	
	
	
}



#endif	// CHANNEL_CONFIG
