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
    private string imu_1_data = null;
    private string imu_2_data = null;
    private string imu_3_data = null;
    private string imu_4_data = null;
    private string speech_data = null;
    private string image_data = null;

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
    //private int curr_level = 0; 
    private int[] combination = new int[4];
    private bool[] time_flag = new bool[4];
    private bool[] panel_passed = new bool[4];
    private double[] start_time = new double[4];
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
        //curr_level = 1; 

        // generate random sequence of numbers  0-9 for 
        // players to try and accomplish
        // initialize private variables
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
            time_flag[i] = false;
            panel_passed[i]=false;
            start_time[i]=0.0;           
            
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
        Debug.Log(ipHost.AddressList[3]);
        //Debug.Log("Hello");
        //Debug.Log(ipHost.AddressList[2]);
        IPAddress ipAddr = ipHost.AddressList[3];
        IPEndPoint localEndPoint = new IPEndPoint(ipAddr, 50000);
        Socket listener = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

        try
        {

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
                    string [] packet = data.Split('*');
                    //Debug.Log(data);
                    
                    imu_1_data = packet[0];                    
                    imu_2_data = packet[1];
                    imu_3_data = packet[2];
                    imu_4_data = packet[3];
                    speech_data = packet[4];
                    image_data = packet[5];
                    Debug.Log(speech_data);
                    
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

        //executes levels 
        // Update function runs even when socket is disconnected
        // We make sure clientSocket is connected 
        //Debug.Log(curr_level); 
        try{
        
            if((clientSocket.Connected == true )){        
                if (imu_1_data != "R1,P1")
                {
                    //converts string to float and converts to combination
                    //Debug.Log(imu_1_data);
                    string [] roll_pitch_parsed = imu_1_data.Split(',');
                    string pitch = roll_pitch_parsed[1];
                    //Debug.Log(pitch);

                    float pitch_float = (float) Convert.ToDouble(pitch);
                    int value = (int) ((pitch_float+20)/10);

                    level_1(value, combination[0]);
                }

                // Client Sockets are already connected no need to check 
                // connection validity

                //if (curr_level == 2)
                //Debug.Log(imu_2_data);
                if (imu_2_data != "R2,P2")
                    {
                        //converts string to float and converts to combination
                        string [] roll_pitch_parsed = imu_2_data.Split(',');
                        string pitch = roll_pitch_parsed[1];
                        //Debug.Log(pitch);

                        float pitch_float = (float) Convert.ToDouble(pitch);
                        int value = (int) ((pitch_float+20)/10);

                        level_2(value, combination[1]);
                    }

                // add player for player 3 
                //if (curr_level == 3)
                if (imu_3_data != "R3,P3")
                    {
                        //converts string to float and converts to combination
                        string [] roll_pitch_parsed = imu_3_data.Split(',');
                        string pitch = roll_pitch_parsed[1];
                        // Debug.Log(pitch);

                        float pitch_float = (float) Convert.ToDouble(pitch);
                        int value = (int) ((pitch_float+20)/10);

                        level_3(value, combination[2]);
                    }

                // add logic for player 4

                //if (curr_level == 4)
                if (imu_4_data != "R4,P4")
                {
                    //converts string to float and converts to combination
                    string [] roll_pitch_parsed = imu_4_data.Split(',');
                    string pitch = roll_pitch_parsed[1];
                    //Debug.Log(pitch);

                    float pitch_float = (float) Convert.ToDouble(pitch);
                    int value = (int) ((pitch_float+20)/10);

                    level_4(value, combination[3]);
                } 
            }
        }
        catch(Exception e){}          

    }

    // Level 1 Execution
    void level_1(float value, int combination)
    {
        if (!panel_passed[0]){
            my_player_script_1.updateName(value.ToString());  
            // compares to find when the values equal
            if (value == combination && !time_flag[0])
            {
                start_time[0] = Time.time;
                time_flag[0] = true;

                // fills the borders of the panel green
                my_panel_script_1.updatePanelGreen(false);
            }
            else if (value != combination)
            {
                time_flag[0] = false; 

                // fills the borrders of the panel red 
                my_panel_script_1.updatePanelRed(false);
            }
            if (time_flag[0])
            {
                double curr_time = Time.time;

                // IMU was held accordingly to the combination
                if((curr_time-start_time[0]) > passed_time )
                {
                    // increase level
                    //curr_level = 2; 

                    // fills the panel green
                    my_panel_script_1.updatePanelGreen(true);
                    my_player_script_1.updateName(value.ToString()); 

                    time_flag[0] = false; 
                    panel_passed[0]=true;
                
                }
            }
        }
        // does nothing
        else{}
    }
    // Level 2 execution    
    void level_2(float value, int combination)
    {
        if (!panel_passed[1]){
            my_player_script_2.updateName(value.ToString());  
            // compares to find when the values equal
            if (value == combination && !time_flag[1])
            {
                start_time[1] = Time.time;
                time_flag[1] = true;

                // fills the borders of the panel green
                my_panel_script_2.updatePanelGreen(false);

            }
            else if (value != combination)
            {
                //Debug.Log("Not correct combination");
                time_flag[1] = false; 

                // fills the borrders of the panel red 
                my_panel_script_2.updatePanelRed(false);
            }
            if (time_flag[1])
            {
                double curr_time = Time.time;

                // IMU was held accordingly to the combination
                if((curr_time-start_time[1]) > passed_time )
                {
                    // increase level
                    //curr_level = 3; 

                    // fills the panel green
                    my_panel_script_2.updatePanelGreen(true);
                    my_player_script_2.updateName(value.ToString());  


                    time_flag[1] = false;
                    panel_passed[1] = true; 
                }
            }
        }
        //do nothing
        else{}
    }



    // Level 3 Execution
    void level_3(float value, int combination)
    {
        if(!panel_passed[2])
        {
            my_player_script_3.updateName(value.ToString());  
            // compares to find when the values equal
            if (value == combination && !time_flag[2])
            {
                start_time[2] = Time.time;
                time_flag[2] = true;

                // fills the borders of the panel green
                my_panel_script_3.updatePanelGreen(false);
            }
            else if (value != combination)
            {
                time_flag[2] = false; 

                // fills the borrders of the panel red 
                my_panel_script_3.updatePanelRed(false);
            }
            if (time_flag[2])
            {
                double curr_time = Time.time;

                // IMU was held accordingly to the combination
                if((curr_time-start_time[2]) > passed_time )
                {
                    // increase level
                    //curr_level = 4; 

                    // fills the panel green
                    my_panel_script_3.updatePanelGreen(true);

                    time_flag[2] = false;
                    panel_passed[2] = true;
                }
            }
        }
        //do nothing
        else{}
    }

     // Level 4 Execution
    void level_4(float value, int combination)
    {
        if (!panel_passed[3])
        {
            my_player_script_4.updateName(value.ToString());  
            // compares to find when the values equal
            if (value == combination && !time_flag[3])
            {
                start_time[3] = Time.time;
                time_flag[3] = true;

                // fills the borders of the panel green
                my_panel_script_4.updatePanelGreen(false);
            }
            else if (value != combination)
            {
                time_flag[3] = false; 

                // fills the borrders of the panel red 
                my_panel_script_4.updatePanelRed(false);
            }
            if (time_flag[3])
            {
                double curr_time = Time.time;

                // IMU was held accordingly to the combination
                if((curr_time-start_time[3]) > passed_time )
                {
                    // increase level
                    //curr_level = 5; 

                    // fills the panel green
                    my_panel_script_4.updatePanelGreen(true);

                    time_flag[3] = false;
                    panel_passed[3] = true; 
                }
            }
        }
        //do nothing
        else{}
    }
    


}
