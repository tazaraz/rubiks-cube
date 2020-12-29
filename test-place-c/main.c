#define F_CPU 16000000UL
#define BAUD 115200
#define __AVR_ATmega2560__

#include <avr/io.h>
#include <util/delay.h>
#include <util/setbaud.h>

void init_uart(void){
	UBRR0H = UBRRH_VALUE;
    UBRR0L = UBRRL_VALUE;

    UCSR0A |= (1 << U2X0);                  // Double the baud rate
    UCSR0C = 6;                             // Data size: 8 bit
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);   // Enable RX and TX
}

void send(char c){
    /* Wait while the USART Data Register (UDR) empty bit is set*/
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = c;
}

char receive(void) {
    while (!(UCSR0A & (1 << RXC0))); /* Wait until data exists. */
    return UDR0;
}

int main(void){
    init_uart();
    for (int i = 0; i < 6; i++){
        char text[] = "Hello World\n";
        for (int h = 0; h < 13; h++)
            // UDR0=text[h];
            send(text[h]);
    }
}