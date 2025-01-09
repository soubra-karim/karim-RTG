#include <stdio.h>
#include <stdlib.h>
#include "cmsis_os.h"                                           // CMSIS RTOS header file
#include "GLCD.h"
#include "KBD.h"
#include "scoobydoo.h"
#include "rshow.h"
#include "mario.h"
#include "luigi.h"


/*----------------------------------------------------------------------------
 *      Thread 1 'Thread_Name': Sample thread
 *---------------------------------------------------------------------------*/

#define __FI        1
#define ITM_Port8(n)    (*((volatile unsigned char *)(0xE0000000+4*n)))
#define ITM_Port16(n)   (*((volatile unsigned short*)(0xE0000000+4*n)))
#define ITM_Port32(n)   (*((volatile unsigned long *)(0xE0000000+4*n)))

#define DEMCR           (*((volatile unsigned long *)(0xE000EDFC)))
#define TRCENA          0x01000000

struct __FILE { int handle;  };
FILE __stdout;
FILE __stdin;

int fputc(int ch, FILE *f) {
  if (DEMCR & TRCENA) {
    while (ITM_Port32(0) == 0);
    ITM_Port8(0) = ch;
  }
  return(ch);
}



int screen_sel=0;
unsigned int startup=0;
uint32_t new_dir = 0U;
uint32_t current_dir=0U;


extern unsigned char Bg_16bpp_l[];
extern unsigned char Bg_16bpp_r[];
extern unsigned char Bg_16bpp_b[];

int points;
void change_screen(int i);
void main_menu();
void photo_gallery();
void switch_pic(int i);
void highlight_option(int i);

void usb_audio();



//game
void hit_the_target_game();
//void instruction();
//void lives_counter(int hit);
int gen_level();
int fire(int player_position, int hole_position); // return 1 if success ,0 to loose lives

int move_player(int i,int dir);

void rscreen();
// may need clear level

void joystick_listen (void const *argument);                             // thread function
osThreadId tid_joystick_listen;                                          // thread id
osThreadDef (joystick_listen, osPriorityNormal, 1, 0);   
void main_thread (void const *argument);                             // thread function
osThreadId tid_main;                                          // thread id
osThreadDef (main_thread, osPriorityNormal, 1, 0);                   // thread object

int Init_Thread (void) {

  tid_main = osThreadCreate (osThread(main_thread), NULL);
	tid_joystick_listen = osThreadCreate (osThread(joystick_listen), NULL);
  if (!tid_main) return(-1);
  
  return(0);
}

void main_thread (void const *argument) {
		if(startup==0){
				GLCD_Init();                               /* Initialize graphical LCD (if enabled */
				

				GLCD_Clear(White);                         /* Clear graphical LCD display   */
				


				KBD_Init();
				change_screen(999);
				startup=1;
		}
  while (1) {
	
		
			
			change_screen(screen_sel);
		
			
  }
}

void joystick_listen (void const *argument) {

  while (1) {
							new_dir=get_button();															// suspend thread
  }
}

void change_screen(int i){
	GLCD_Clear(White);
	if(i==999){
		main_menu();
	}if(i==0){
		GLCD_Clear(White);
		switch_pic(999);
		photo_gallery();
		
	}else if(i==1){
		
			
		
				GLCD_SetBackColor(Blue);
				GLCD_SetTextColor(White);
				GLCD_DisplayString(1, 0, __FI, "       in mp3     ");
		
				 usb_audio();
	}else if(i==2){
		
		
		
		GLCD_SetBackColor(Blue);
		GLCD_SetTextColor(White);
		hit_the_target_game();
	}
	
}



void hit_the_target_game(){
	
	int hit_or_miss;
	uint32_t prev_dir=0U;
	for(;;){
						GLCD_Clear(White);
						GLCD_SetBackColor(White);
						GLCD_SetTextColor(Black);
						points=0;
//						lives=3;
					//	instruction();
						 //int restart_screen =0;
							
				
						for(;;){
						
							
							GLCD_Clear(White);
							int hole = gen_level();
							int player_y=5;
							
							GLCD_DisplayString(player_y,3, __FI, ">");
							
							
							for(;;){
								if(new_dir!=prev_dir){
									prev_dir=new_dir;
									
									if(new_dir==0x08){ //move up
										player_y=move_player(player_y,0);
										
									}else if (new_dir == 0x10) // right -> fire
									{
										//hit_or_miss=fire(player_y,hole);// return 1 if success ,0 to loose lives
										fire(player_y,hole);
										//lives_counter(hit_or_miss);
									  /*if(lives<0){
												restart_screen=1;
											}*/
										break;
									}else if (new_dir ==0x20) // move down
									{
										player_y=move_player(player_y,1);
									}
									else if (new_dir ==0x40) // left means back to home
									{
										screen_sel=999;
										break;
									
									}
								}
							}
							
							
							/*if(screen_sel==999 || restart_screen==1){
								break;
							}*/
							if(screen_sel==999){
											break;
					
							}	
						}
					if(screen_sel==999){
						break;
					
					}
					

	}

	
}


void usb_audio(){
		
	for(;;){
	

									
									
				if (new_dir ==0x40){
					
					screen_sel=999;
					break;
									
				}
		}
	}

/*
void instruction(){
			GLCD_DisplayString(1, 3, __FI, "welcome to Hit the target!");
			GLCD_DisplayString(2, 3, __FI, "Intrustions");
			GLCD_DisplayString(3, 3, __FI, "fire -> right");
			GLCD_DisplayString(4, 3, __FI, "Move-> up and down");
			GLCD_DisplayString(5, 3, __FI, "quit->left");
			osDelay(10000);
	
}
void lives_counter(int hit){
	
	char text[20];
	sprintf(text,"%d",points);
	GLCD_Clear(White); 
	if(hit==0 && lives>=0){
			lives--;
			GLCD_DisplayString(2, 3, __FI, "MISS");
			GLCD_DisplayString(3, 3, __FI, "LIVES REMAINING:");
			GLCD_DisplayString(5, 3, __FI, "points:");
			GLCD_DisplayString(6, 3, __FI, (unsigned char *)text);
		if(lives==2){
			GLCD_DisplayString(4, 3, __FI, "XX");
			
		}else if(lives==1){
			GLCD_DisplayString(4, 3, __FI, "X");

		}else if(lives==0){
			GLCD_DisplayString(4, 3, __FI, "0");
		}
		
	}else if(hit==1 && lives>=0){
				points++;
				GLCD_DisplayString(3, 3, __FI, "MISS");
				GLCD_DisplayString(4, 3, __FI, "LIVES REMAINING:");
				GLCD_DisplayString(5, 3, __FI, "points");
				GLCD_DisplayString(6, 3, __FI, (unsigned char *)text);
		if(lives==3){
				GLCD_DisplayString(5, 3, __FI, "XXX");
		}else if(lives==2){
				GLCD_DisplayString(5, 3, __FI, "XX");
		}else if(lives==1){
			GLCD_DisplayString(5, 3, __FI, "X");
		}else if(lives==0){
			GLCD_DisplayString(5, 3, __FI, "0");

		}
	}
	if(lives<0){
		GLCD_Clear(White);
		GLCD_DisplayString(3, 3, __FI, "GAME OVER");
		
	}
	
		osDelay(10000);
	
}*/
int fire(int player_position, int hole_position){
	
	for(int i=4; i<17;i++){
		if(player_position==hole_position){
			GLCD_DisplayString(player_position, i-1, __FI, " ");
			GLCD_DisplayString(player_position, i, __FI, ">");
		}else{
			if(i<=12){
				GLCD_DisplayString(player_position, i-1, __FI, " ");
				GLCD_DisplayString(player_position, i, __FI, ">");
			}
		}
	}
	
	if(player_position==hole_position){
		GLCD_DisplayString(player_position,17, __FI, " ");
		return 1;
	}else{
		GLCD_DisplayString(player_position, 12, __FI, ">");
		return 0;
	}
}
int move_player(int i,int dir){
	int curr_pos=i;
	if(dir==1){ // moves player down
		if(i==9){
			i=9;
		}else{
			i++;
		}
		
	}else if(dir==0){
		if(i==0){
			i=0;
		}else{
			i--;
		}
	}
	
	GLCD_DisplayString(curr_pos, 3, __FI, " ");
	GLCD_DisplayString(i,3,__FI,">");
	
	return i; //return updated position
}

int gen_level(){
	int hole=rand()%10;
	
	for(int i=0 ; i <=9;i++){
		
		
		if(i!=hole){
			GLCD_DisplayString(i,15,__FI,"|");
		}
		
	}
	return hole;
}
void main_menu(){
			int current_sel=0;
			highlight_option(current_sel);
			for(;;){
				
				//if(new_dir!=current_dir){
				//	current_dir=new_dir;
					
					if (new_dir == 0x08) // up
					{
							if(current_sel==0){
								current_sel=0;
							}else{
								current_sel--;
							}
							highlight_option(current_sel);
						
						
					}
					else if (new_dir == 0x10) // right
					{
						screen_sel=current_sel;
						//change_screen(screen_sel);
						break;
				
					}
					else if (new_dir ==0x20) // down
					{
						if(current_sel==2){
							current_sel=2;
						}else{
							current_sel++;
						}
						highlight_option(current_sel);
					
					}
				}
			//}
}


void highlight_option(int i){
		
		
		GLCD_SetBackColor(White);
		GLCD_SetTextColor(Blue);
		GLCD_DisplayString(1, 5, __FI, "Main Menu");
		if(i==0){
		
			GLCD_SetTextColor(Green);
			GLCD_DisplayString(2, 0, __FI, "       Gallery        ");
			
		
			GLCD_SetTextColor(Blue);
			GLCD_DisplayString(3, 0, __FI, "       MP3            ");
		
		
			GLCD_SetTextColor(Blue);
			GLCD_DisplayString(4, 0, __FI, "       GAME           ");
		}else if(i==1){
		
			GLCD_SetTextColor(Blue);
			GLCD_DisplayString(2, 0, __FI, "       Gallery        ");
			
			GLCD_SetTextColor(Green);
			GLCD_DisplayString(3, 0, __FI, "       MP3            ");
		
			GLCD_SetTextColor(Blue);
			GLCD_DisplayString(4, 0, __FI, "       GAME           ");
		}else if(i==2){
			
			GLCD_SetTextColor(Blue);
			GLCD_DisplayString(2, 0, __FI, "       Gallery        ");
	
			GLCD_SetTextColor(Blue);
			GLCD_DisplayString(3, 0, __FI, "       MP3            ");

			GLCD_SetTextColor(Green);
			GLCD_DisplayString(4, 0, __FI, "       GAME           ");
		}
		
		

				
}

void switch_pic(int i){

  GLCD_Clear(White);
	switch(i){
		case 0:
			GLCD_Clear(White);
			GLCD_Bitmap (  100,   100, 100,  100, SCOOBYDOO_PIXEL_DATA );
			break;
		case 1:
			GLCD_Clear(White);
			GLCD_Bitmap ( 100,   100, 60,  29, RSHOW_PIXEL_DATA  );
			break;
		case 2:
			GLCD_Clear(White);
			GLCD_Bitmap (100,   100, 60,  76, MARIO_PIXEL_DATA);
			break;
		case 3:
			GLCD_Clear(White);
			GLCD_Bitmap (  100, 100, 60,  72, LUIGI_PIXEL_DATA);
			break;
		default:
			GLCD_Clear(White);
			GLCD_Bitmap (  100,   100, 100,  100, SCOOBYDOO_PIXEL_DATA );
			break;
				
		}
	
	
}

void photo_gallery(){
	
			int curr_pic=0;
			
			new_dir=0U;
			current_dir=0U;
			for(;;){
				
				
				if(current_dir!=new_dir){
					current_dir=new_dir;
					if(new_dir==0x40){
						curr_pic--;
						
						if(curr_pic<0){
							curr_pic=0;
						}
							switch_pic(curr_pic);
					}else if (new_dir == 0x10) // right
					{
						curr_pic++;
						
						if(curr_pic>3){
							curr_pic=3;
						}
							switch_pic(curr_pic);
				
					}
					else if (new_dir ==0x20) // down
					{
						screen_sel=999;
						break;
					
					}
					
				
					
				}
			}
}