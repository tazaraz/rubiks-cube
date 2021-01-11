#define F_CPU 16000000UL
#define BAUD 230400
#define __AVR_ATmega2560__

#include <avr/io.h>
#include <util/delay.h>
#include <util/twi.h>
#include <util/setbaud.h>
#include <avr/interrupt.h>
#include "ov7670.h"

void init_pins(){
    cli();  //disable interrupts

    /* Camera Pins */
	// Setup the 8mhz PWM clock on pin 13
	DDRB |= (_BV(PIN7));

	// Disable the external clock (if present) and asynchronous mode
	ASSR &= ~(_BV(EXCLK) | _BV(AS2));

	// Build a waveform for the PWM
	TCCR1A = (_BV(COM0A0) | _BV(WGM01) | _BV(WGM00));
	TCCR1B = (_BV(WGM02)  | _BV(CS00));
	OCR1A  = 0;

    // Set pins 22-29 as input
    DDRA &= ~0b11111111;

    // Set pins 34 (PLCK) and 35 (VSYNC) to input
    DDRC &= ~0b00110000;

    // Set pins 20 and 21 to output
    DDRD |= 0b00000011;

	// Set up the TWI (Two Wire Interface) for 100khz
	TWSR &= ~3;   // Sets the prescaler to 1
	TWBR = 72;    // Value to set speed to 100khz

    /* Serial Communication */
    // UBRR0L can be set manually if preferred.
    // 0 = 2M baud rate. 1 = 1M baud. 3 = 0.5M. 7 = 250k 207 is 9600 baud rate.
    UBRR0L = UBRRL_VALUE;
    UBRR0H = UBRRH_VALUE;

    UCSR0A |= (_BV(U2X0));                  // Double the baud rate
    UCSR0C = 6;                             // Data size: 8 bit
    UCSR0B = (_BV(RXEN0)) | (_BV(TXEN0));   // Enable RX and TX
}

void send(char text[]){
	int h = 0, l = strlen(text);
    for (; h < l; h++)
        send_serial(text[h]);
}

void send_serial(char c){
    /* Wait while the USART Data Register (UDR) empty bit is set*/
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = c;
}

static void captureImg(uint16_t wg,uint16_t hg){
	uint16_t lg2;
	//Wait for vsync it is on pin 45 (counting from 0) portD
    while(!(PINC&(1<<3)));//wait for high
	while((PINC&(1<<3)));//wait for low
    uint8_t buf[320];

    // while(hg--){
    //     send("R");
	// 	lg2=wg;
	// 	while(lg2--){
	// 		while((PINC&(1<<2)));//wait for low
	// 		UDR0=PINA&255;
	// 		while(!(PINC&(1<<2)));//wait for high
	// 	}
	// }

	while(hg--){
		uint8_t*b=buf,*b2=buf;
		lg2=wg/5;
		while(lg2--){
			while((PINC&(1<<2)));//wait for low
			*b++=PINA&255;
			while(!(PINC&(1<<2)));//wait for high
			while((PINC&(1<<2)));//wait for low
			*b++=PINA&255;
			while(!(PINC&(1<<2)));//wait for high
			while((PINC&(1<<2)));//wait for low
			*b++=PINA&255;
			while(!(PINC&(1<<2)));//wait for high
			while((PINC&(1<<2)));//wait for low
			*b++=PINA&255;
			while(!(PINC&(1<<2)));//wait for high
			while((PINC&(1<<2)));//wait for low
			*b++=PINA&255;
			UDR0=*b2++;
			while(!(PINC&(1<<2)));//wait for high
		}
		/* Finish sending the remainder during blanking */
		lg2=320-(wg/5);
		while(!( UCSR0A & (1<<UDRE0)));//wait for byte to transmit
		while(lg2--){
			UDR0=*b2++;
			while(!( UCSR0A & (1<<UDRE0)));//wait for byte to transmit
		}
	}
}

int main(void){
    init_pins();
    camInit();

    setRes(QQVGA);
	setColorSpace(YUV422);
	wrReg(0x11,10);

	send("RDY");
    while (1){
		/* captureImg operates in bytes not pixels in some cases pixels are two bytes per pixel
		 * So for the width (if you were reading 640x480) you would put 1280 if you are reading yuv422 or rgb565 */
		// uint8_t x=63;//Uncomment this block to test divider settings note the other line you need to uncomment
        // do{
        //     wrReg(0x11,x);
        //     _delay_ms(1000);
        //     captureImg(160*2,120);
        //     // captureImg(640*2,480);
		// }while(--x);//Uncomment this line to test divider settings
        captureImg(160*2,120);
        // captureImg(640,480);
	}
}
