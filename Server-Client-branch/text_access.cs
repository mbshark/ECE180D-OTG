using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;




public class text_access : MonoBehaviour
{
    //contents for tcp connection
    private string roll = null;
    private string pitch = null; 
    private Socket clientSocket; 


    // creates an object to each players game display
    public GameObject my_combination;  
    public GameObject my_player_1;
    public GameObject my_player_2;
    public GameObject my_player_3;
    public GameObject my_player_4;

    //Panel color access
    public GameObject my_panel_1;
    public GameObject my_panel_2;
    public GameObject my_panel_3;
    public GameObject my_panel_4;

    //gain access to the script to change text in real time 
    combination_display my_combination_script; 
    imu_1 my_player_script_1;
    imu_2 my_player_script_2;
    imu_3 my_player_script_3;
    imu_4 my_player_script_4;
    // gain access to the script to change panel color in real time
    panel_player_1 my_panel_script_1;
    panel_player_2 my_panel_script_2;
    panel_player_3 my_panel_script_3;
    panel_player_4 my_panel_script_4;

    //Game variables 
    private int curr_level = 0; 
    private int[] combination = new int[4];
    private bool time_flag = false; 
    private double start_time = 0.0; 
    private double passed_time = 1.5; //time required to pass the level 


    void Start()
    {
        // Usually the server doesn't need to draw anything on the screen
        Thread thr2 = new Thread(CreateServer);
        thr2.Start();


        // Gathers the object instant for the script
        my_combination_script= my_combination.GetComponent<combination_display>(); 
        my_player_script_1 = my_player_1.GetComponent<imu_1>();
        my_player_script_2 = my_player_2.GetComponent<imu_2>();
        my_player_script_3 = my_player_3.GetComponent<imu_3>();
        my_player_script_4 = my_player_4.GetComponent<imu_4>();
        my_panel_script_1 = my_panel_1.GetComponent<panel_player_1>();
        my_panel_script_2 = my_panel_2.GetComponent<panel_player_2>();
        my_panel_script_3 = my_panel_3.GetComponent<panel_player_3>();
        my_panel_script_4 = my_panel_4.GetComponent<panel_player_4>();

        // start at level one 
        curr_level = 1; 

        // generate random sequence of numbers  0-9 for 
        // players to try and accomplish
        int min_num = 0;
        int max_num = 9; 
        string comb = "Complete this Combination\n\t\t\t\t";
        for (int i = 0; i < combination.Length; i++)
        {
            combination[i]= UnityEngine.Random.Range(min_num,max_num);
            if(i < combination.Length-1)
            {
                comb += combination[i].ToString() + "-";
            }
            else
            {
                comb += combination[i].ToString(); 
            }
            
            
        }


        // Starts all players at combination zero
        my_combination_script.updateName(comb);
        my_player_script_1.updateName("0");  
        my_player_script_2.updateName("0");  
        my_player_script_3.updateName("0");  
        my_player_script_4.updateName("0");

        
    }

    void CreateServer()
    {
        IPHostEntry ipHost = Dns.GetHostEntry(Dns.GetHostName());
        //Debug.Log(ipHost.AddressList[0]);
        Debug.Log(ipHost.AddressList[3]);
        //Debug.Log("Hello");
        //Debug.Log(ipHost.AddressList[2]);
        IPAddress ipAddr = ipHost.AddressList[3];
        Debug.Log(ipAddr.AddressFamily);
        IPEndPoint localEndPoint = new IPEndPoint(ipAddr, 5005);
        Socket listener = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

        try
        {

            Debug.Log("Bind");

            // Using Bind() method we associate a 
            // network address to the Server Socket 
            // All client that will connect to this  
            // Server Socket must know this network 
            // Address 
            listener.Bind(localEndPoint);

            // Using Listen() method we create  
            // the Client list that will want 
            // to connect to Server
            listener.Listen(10);

            while (true)
            {

                Debug.Log("Waiting connection ... ");

                // Suspend while waiting for 
                // incoming connection Using  
                // Accept() method the server  
                // will accept connection of client 
                clientSocket = listener.Accept();

                Debug.Log("Connected");

                // Data buffer 
                byte[] bytes = new Byte[1024];

                while (true)
                {
                    int numByte = clientSocket.Receive(bytes);

                    string data = Encoding.ASCII.GetString(bytes,
                                               0, numByte);
                   // Debug.Log(data);

                    if (data[0] == 'd'){
	                    string[] words = data.Split(',');
	                    roll = words[1];
	                    pitch = words[2];

	                    if (data.IndexOf("#") > -1)
	                    {
	                        Debug.Log("failed");
	                        break;
	                    }
	                } else if (data[0] == 'S'){
	                	Debug.Log(data);
                        string[] words = data.Split(',');
	                	string cmd = words[1];
	                	Debug.Log(cmd);
	                	string msg = "";
	                	if (cmd.Equals("hint")){
	                		msg = "Here is a very useful hint";
	                	} else if (cmd.Equals("play")) {
	                		msg = "Resume the game";
						} else if (cmd.Equals("pause")){
							msg = "Game is now PAUSED";
						} else {
							msg = "Client sent invalid command";
						}
						Debug.Log(msg);
	                }
                    
                }

                //Debug.Log(data);
                //byte[] message = Encoding.ASCII.GetBytes("Test Server");

                // Send a message to Client  
                // using Send() method 
                // clientSocket.Send(message);

                // Close client Socket using the 
                // Close() method. After closing, 
                // we can use the closed Socket  
                // for a new Client Connection 

                Debug.Log("Closing Connection");
                clientSocket.Shutdown(SocketShutdown.Both);
                clientSocket.Close();
                Debug.Log("Connection Closed");
                
                break;
            }
        }
        catch (Exception e)
        {
            Debug.Log("exception");
            Console.WriteLine(e.ToString());
        }

    }
    // Update is called once per frame
    // Updates the text that is shown for the game
    void Update()
    {
        //converts string to float and converts to combination
        float pitch_float = (float) Convert.ToDouble(pitch);
        int value = (int) ((pitch_float+20)/10);

        //executes levels 
        try
        {
            // Update function runs even when socket is disconnected
            // hence why i am checking for the socket connection
            // before the levels executes 
            if(curr_level == 1 && clientSocket.Connected == true)
            {            
                level_1(value, combination[curr_level-1]);
            }
        }
        catch(Exception e)
        {}

        // Client Sockets are already connected no need to check 
        // connection validity

        if (curr_level == 2)
        {
            level_2(value, combination[curr_level-1]); 
        }

        if (curr_level == 3)
        {
            level_3(value, combination[curr_level-1]); 
        }

        if (curr_level == 4)
        {
            level_4(value, combination[curr_level-1]); 
        }   

    }

    // Level 1 Execution
    void level_1(float value, int combination)
    {
        my_player_script_1.updateName(value.ToString());  
        // compares to find when the values equal
        if (value == combination && !time_flag)
        {
            start_time = Time.time;
            time_flag = true;

            // fills the borders of the panel green
            my_panel_script_1.updatePanelGreen(false);
        }
        else if (value != combination)
        {
            time_flag = false; 

            // fills the borrders of the panel red 
            my_panel_script_1.updatePanelRed(false);
        }
        if (time_flag)
        {
            double curr_time = Time.time;

            // IMU was held accordingly to the combination
            if((curr_time-start_time) > passed_time )
            {
                // increase level
                curr_level = 2; 

            // fills the panel green
            my_panel_script_1.updatePanelGreen(true);
            my_player_script_1.updateName(value.ToString()); 

            time_flag = false; 
            
            }
        }
    }
    // Level 2 execution    
    void level_2(float value, int combination)
    {
        my_player_script_2.updateName(value.ToString());  
        // compares to find when the values equal
        if (value == combination && !time_flag)
        {
            start_time = Time.time;
            time_flag = true;

            // fills the borders of the panel green
            my_panel_script_2.updatePanelGreen(false);

        }
        else if (value != combination)
        {
            //Debug.Log("Not correct combination");
            time_flag = false; 

            // fills the borrders of the panel red 
            my_panel_script_2.updatePanelRed(false);
        }
        if (time_flag)
        {
            double curr_time = Time.time;

            // IMU was held accordingly to the combination
            if((curr_time-start_time) > passed_time )
            {
                // increase level
                curr_level = 3; 

                // fills the panel green
                my_panel_script_2.updatePanelGreen(true);
                my_player_script_2.updateName(value.ToString());  


                time_flag = false; 
            }
        }
    }

    // Level 3 Execution
    void level_3(float value, int combination)
    {
        my_player_script_3.updateName(value.ToString());  
        // compares to find when the values equal
        if (value == combination && !time_flag)
        {
            start_time = Time.time;
            time_flag = true;

            // fills the borders of the panel green
            my_panel_script_3.updatePanelGreen(false);
        }
        else if (value != combination)
        {
            time_flag = false; 

            // fills the borrders of the panel red 
            my_panel_script_3.updatePanelRed(false);
        }
        if (time_flag)
        {
            double curr_time = Time.time;

            // IMU was held accordingly to the combination
            if((curr_time-start_time) > passed_time )
            {
                // increase level
                curr_level = 4; 

                // fills the panel green
                my_panel_script_3.updatePanelGreen(true);

                time_flag = false; 
            }
        }
    }

     // Level 4 Execution
    void level_4(float value, int combination)
    {
        my_player_script_4.updateName(value.ToString());  
        // compares to find when the values equal
        if (value == combination && !time_flag)
        {
            start_time = Time.time;
            time_flag = true;

            // fills the borders of the panel green
            my_panel_script_4.updatePanelGreen(false);
        }
        else if (value != combination)
        {
            time_flag = false; 

            // fills the borrders of the panel red 
            my_panel_script_4.updatePanelRed(false);
        }
        if (time_flag)
        {
            double curr_time = Time.time;

            // IMU was held accordingly to the combination
            if((curr_time-start_time) > passed_time )
            {
                // increase level
                curr_level = 5; 

                // fills the panel green
                my_panel_script_4.updatePanelGreen(true);

                time_flag = false; 
            }
        }
    }


}
