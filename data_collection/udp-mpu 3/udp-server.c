/*
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */

#include "contiki.h"
#include "contiki-lib.h"
#include "contiki-net.h"
#include "dev/leds.h"
#include "dev/serial-line.h"
#include "contiki.h"
#include "sys/etimer.h"
#include "sys/ctimer.h"
#include "dev/leds.h"
#include "dev/watchdog.h"
#include "random.h"
#include "board-peripherals.h"
#include "contiki-conf.h"
#include "lib/sensors.h"
#include "mpu-9250-sensor.h"
#include "sys/rtimer.h"
#include "sensor-common.h"
#include "board-i2c.h"
#include "sys/timer.h"
#include "sys/rtimer.h"	
#include "ti-lib.h"
#include "dev/leds.h"
#include "button-sensor.h"	
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
#include <stdint.h>
#include "contiki-net.h"
#include "net/ip/uip-debug.h"
#include <string.h>

//#define DEBUG DEBUG_PRINT


#define UIP_IP_BUF   ((struct uip_ip_hdr *)&uip_buf[UIP_LLH_LEN])
#define MAX_PAYLOAD_LEN 120
#define FREQUENCY 160 // in Hz
#define READING_TIME 2 // in seconds
#define BYTES_PER_PACKET 64 // make sure READING_TIME*FREQUENCY is dividable by BYTES_PER_PACKET
#define TIME_BETWEEN_PACKETS 1000 // in milliseconds
static struct uip_udp_conn *server_conn;


int readings[FREQUENCY*READING_TIME];
int num_readings;
int packets_send;

static struct rtimer timer_rtimer;
static rtimer_clock_t timeout_rtimer = RTIMER_SECOND / FREQUENCY;
static struct ctimer timer_ctimer;

void measurement_callback(struct rtimer *timer, void *ptr) {
  	readings[num_readings] = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Z);
	if(num_readings % 20 == 0){
		printf("reading %d value %d \n\r", num_readings, readings[num_readings]);
	}
	num_readings++;

	/* Re-arm rtimer */
	if(num_readings < FREQUENCY*READING_TIME){
		rtimer_set(&timer_rtimer, RTIMER_NOW() + timeout_rtimer, 0, measurement_callback, NULL);
	}
}

int inc = 0;
void send_callback(){
        uip_ipaddr_t target_addr;
        uip_ip6addr(&target_addr, 0xaaaa, 0, 0, 0, 0, 0, 0, 1);
	int final_val = 1;
	int num_packets_to_send = (FREQUENCY*READING_TIME)/(BYTES_PER_PACKET/4);
	if (packets_send < num_packets_to_send) {
		uip_udp_packet_sendto(server_conn, readings+(16*packets_send), 64, &target_addr, UIP_HTONS(47371));
		printf("Send finished for the packet[%d] \n\r", packets_send);
		ctimer_set(&timer_ctimer, 1 * CLOCK_SECOND, send_callback, NULL);
	}

	if (packets_send == num_packets_to_send) {
		uip_udp_packet_sendto(server_conn, &final_val, 4, &target_addr, UIP_HTONS(47371));
		printf("Final Send finished \n\r");
		leds_off(LEDS_GREEN);
	}

	packets_send++;
}


PROCESS(udp_server_process, "UDP server process");
AUTOSTART_PROCESSES(&resolv_process,&udp_server_process);
/*---------------------------------------------------------------------------*/
/*---------------------------------------------------------------------------*/
static void
print_local_addresses(void)
{
  int i;
  uint8_t state;

  PRINTF("Server IPv6 addresses: ");
  for(i = 0; i < UIP_DS6_ADDR_NB; i++) {
    state = uip_ds6_if.addr_list[i].state;
    if(uip_ds6_if.addr_list[i].isused &&
       (state == ADDR_TENTATIVE || state == ADDR_PREFERRED)) {
      PRINT6ADDR(&uip_ds6_if.addr_list[i].ipaddr);
      PRINTF("\n\r");
    }
  }
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_server_process, ev, data)
{
#if UIP_CONF_ROUTER
  uip_ipaddr_t ipaddr;
#endif /* UIP_CONF_ROUTER */

  PROCESS_BEGIN();
  PRINTF("UDP server started\n\r");

#if RESOLV_CONF_SUPPORTS_MDNS
  resolv_set_hostname("contiki-udp-server");
#endif

#if UIP_CONF_ROUTER
  uip_ip6addr(&ipaddr, 0xaaaa, 0, 0, 0, 0, 0, 0, 0);
  uip_ds6_set_addr_iid(&ipaddr, &uip_lladdr);
  uip_ds6_addr_add(&ipaddr, 0, ADDR_AUTOCONF);
#endif /* UIP_CONF_ROUTER */

  print_local_addresses();

  //Create UDP socket and bind to port 3000
  // updated to allow connections from any src port
  server_conn = udp_new(NULL, UIP_HTONS(0), NULL);
  udp_bind(server_conn, UIP_HTONS(3000));


  SENSORS_ACTIVATE(mpu_9250_sensor);
  // power up and initialise accelerometer
  mpu_9250_sensor.configure(SENSORS_ACTIVE, MPU_9250_SENSOR_TYPE_ACC_Z);



  while(1) {
	PROCESS_YIELD();

	if(ev == sensors_event && data == &button_left_sensor) {

		//Check if left push button event has occured
		if(data == &button_left_sensor) {
			printf("Collecting z-axis accelerometer values...\n\r");
			leds_on(LEDS_GREEN);

			num_readings = 0;
			packets_send = 0;
			rtimer_set(&timer_rtimer, RTIMER_NOW() + timeout_rtimer, 0, measurement_callback, NULL);	
			ctimer_set(&timer_ctimer, (READING_TIME+0.5) * CLOCK_SECOND, send_callback, NULL);

		}
	}
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
