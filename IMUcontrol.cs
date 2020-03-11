using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using TMPro;




public class IMUcontrol : MonoBehaviour
{
    //contents for tcp connection
    private string imu_1_data = null;
    private string imu_2_data = null;
    private string imu_3_data = null;
    private string imu_4_data = null;
    private string speech_data = null;
    private string image_data = null;
    
    public bool UnlockR1=false;
    
    public int R2State=0;
    public bool showBanana=false;
    public bool showRing=false;
    public bool showUmbrella=false;
    public bool showIron=false;
    public bool showNotebook=false;
    public bool UnlockR2=false;

    public bool UnlockR3=false;


    private Socket clientSocket;

    private string[] riddles={
        "Chimpanzee snack",
        "If you like it you better...",
        "Rihanna in the rain",
        "how to press a shirt",
        "Important school supply",
        ""
    };

    private int HexCount=0;
    private int PentCount=0;
    private int RectCount=0;
    private int TriCount=0;

    // creates an object to each players game display 
    public GameObject my_player_1;
    public GameObject my_player_2;
    public GameObject my_player_3;
    public GameObject my_player_4;

    public GameObject riddleObj;
    public TextMeshPro riddleText;

    //gain access to the script to change text in real time 
    changeDigit1 my_player_script_1;
    changeDigit2 my_player_script_2;
    changeDigit3 my_player_script_3;
    changeDigit4 my_player_script_4;

    private GameObject Q1;
    private GameObject Q2;
    private GameObject Q3;
    private GameObject Q4;

    private TextMeshPro Q1text;
    private TextMeshPro Q2text;
    private TextMeshPro Q3text;
    private TextMeshPro Q4text;

    private bool holdQ1= false;
    private bool holdQ2= false;
    private bool holdQ3= false;
    private bool holdQ4= false;


    
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
        my_player_script_1 = my_player_1.GetComponent<changeDigit1>();
        my_player_script_2 = my_player_2.GetComponent<changeDigit2>();
        my_player_script_3 = my_player_3.GetComponent<changeDigit3>();
        my_player_script_4 = my_player_4.GetComponent<changeDigit4>();

        riddleObj=GameObject.Find("Riddle");
        riddleText= riddleObj.GetComponent<TextMeshPro>();

        Q1=GameObject.Find("Q1");
        Q2=GameObject.Find("Q2");
        Q3=GameObject.Find("Q3");
        Q4=GameObject.Find("Q4");

        Q1text=Q1.GetComponent<TextMeshPro>();
        Q2text=Q2.GetComponent<TextMeshPro>();
        Q3text=Q3.GetComponent<TextMeshPro>();
        Q4text=Q4.GetComponent<TextMeshPro>();

        Q1text.SetText("1");
        Q2text.SetText("2");
        Q3text.SetText("3");
        Q4text.SetText("4");

        // start at level one 
        //curr_level = 1; 

        // generate random sequence of numbers  0-9 for 
        // players to try and accompli



        // Starts all players at combination zero
        my_player_script_1.setDigit1("1");  
        my_player_script_2.setDigit2("1");  
        my_player_script_3.setDigit3("1");  
        my_player_script_4.setDigit4("1");
        riddleText.SetText(riddles[0]);


        
    }

    void CreateServer()
    {
        IPHostEntry ipHost = Dns.GetHostEntry(Dns.GetHostName());
        Debug.Log(ipHost.AddressList[0]);
        //Debug.Log("Hello");
        //Debug.Log(ipHost.AddressList[2]);
        IPAddress ipAddr = ipHost.AddressList[0];
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

                    level_1(value);
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

                        level_2(value);
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

                        level_3(value);
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

                    level_4(value);
                } 
                if (panel_passed[0]&&panel_passed[1]&&panel_passed[2]&&panel_passed[3])
                {
                    UnlockR1=true;
                }

                if (speech_data != "")
                {
                    string[] commands={"banana", "ring", "umbrella", "iron", "notebook", "Bruin"};

                    if (speech_data==commands[R2State]){
                        switch (R2State) {
                            case 0: 
                                showBanana=true;
                                riddleText.SetText(riddles[1]);
                                R2State=1;
                                break;
                            case 1:
                                showRing=true;
                                riddleText.SetText(riddles[2]);
                                R2State=2;
                                break;
                            case 2:
                                showUmbrella=true;
                                riddleText.SetText(riddles[3]);
                                R2State=3;
                                break;
                            case 3:
                                showIron=true;
                                riddleText.SetText(riddles[4]);
                                R2State=4;
                                break;
                            case 4:
                                showNotebook=true;
                                riddleText.SetText(riddles[5]);
                                R2State=5;
                                break;
                            case 5:
                                UnlockR2=true;
                                break;
                            default:
                                Debug.Log("R2state="+ R2State);
                                break;
                        }
                    }

                }

                if (Q1text.text=="7")
                {
                    HexCount++;
                } else {
                    HexCount=0;
                }

                if (Q2text.text=="7")
                {
                    PentCount++;
                } else {
                    PentCount=0;
                }
                if (Q3text.text=="7")
                {
                    RectCount++;
                } else {
                    RectCount=0;
                }
                if (Q4text.text=="7")
                {
                    TriCount++;
                } else {
                    TriCount=0;
                }

                if (HexCount==4 && PentCount==4 && RectCount==4 && TriCount==4)
                {
                    UnlockR3=true;
                }
                string [] shape_data=image_data.Split('$');
                if (HexCount<5)
                {
                    switch (shape_data[0].Substring(1,1))
                    {
                        case "T":
                            Q1text.SetText("4");
                            break;
                        case "R":
                            Q1text.SetText("5");
                            break;
                        case "P":
                            Q1text.SetText("6");
                            break;
                        case "H":
                            Q1text.SetText("7");
                            break;
                        case "N":
                            Q1text.SetText("1");
                            break;
                        default:
                            Debug.Log(shape_data[0]);
                            break;

                    }
                }
                if (PentCount<5)
                {
                    switch (shape_data[1].Substring(1,1))
                    {
                        case "T":
                            Q2text.SetText("5");
                            break;
                        case "R":
                            Q2text.SetText("6");
                            break;
                        case "P":
                            Q2text.SetText("7");
                            break;
                        case "H":
                            Q2text.SetText("8");
                            break;
                        case "N":
                            Q2text.SetText("2");
                            break;
                        default:
                            Debug.Log(shape_data[1].Substring(1,1));
                            break;

                    }
                }
                if (RectCount<5)
                {
                    switch (shape_data[2].Substring(1,1))
                    {
                        case "T":
                            Q3text.SetText("6");
                            break;
                        case "R":
                            Q3text.SetText("7");
                            break;
                        case "P":
                            Q3text.SetText("8");
                            break;
                        case "H":
                            Q3text.SetText("9");
                            break;
                        case "N":
                            Q3text.SetText("3");
                            break;
                        default:
                            Debug.Log(shape_data[2].Substring(1,1));
                            break;

                    }
                }
                if (TriCount<5)
                {
                    switch (shape_data[3].Substring(1,1))
                    {
                        case "T":
                            Q4text.SetText("7");
                            break;
                        case "R":
                            Q4text.SetText("8");
                            break;
                        case "P":
                            Q4text.SetText("9");
                            break;
                        case "H":
                            Q4text.SetText("10");
                            break;
                        case "N":
                            Q4text.SetText("4");
                            break;
                        default:
                            Debug.Log(shape_data[3].Substring(1,1));
                            break;

                    }
                }

            }
        }
        catch(Exception e){}          

    }

    // Level 1 Execution
    void level_1(float value)
    {
    	int combination=6;
        if (!panel_passed[0]){
            my_player_script_1.setDigit1(value.ToString());  
            // compares to find when the values equal
            if (value == combination && !time_flag[0])
            {
                start_time[0] = Time.time;
                time_flag[0] = true;

            }
            else if (value != combination)
            {
                time_flag[0] = false; 


            }
            if (time_flag[0])
            {
                double curr_time = Time.time;

                // IMU was held accordingly to the combination
                if((curr_time-start_time[0]) > passed_time )
                {
                    // increase level
                    //curr_level = 2; 

 

                    time_flag[0] = false; 
                    panel_passed[0]=true;

                
                }
            }
        }
        // does nothing
        else{}
    }
    // Level 2 execution    
    void level_2(float value)
    {
    	int combination=4;
        if (!panel_passed[1]){
            my_player_script_2.setDigit2(value.ToString());  
            // compares to find when the values equal
            if (value == combination && !time_flag[1])
            {
                start_time[1] = Time.time;
                time_flag[1] = true;

            }
            else if (value != combination)
            {
                //Debug.Log("Not correct combination");
                time_flag[1] = false; 

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



                    time_flag[1] = false;
                    panel_passed[1] = true; 
                }
            }
        }
        //do nothing
        else{}
    }



    // Level 3 Execution
    void level_3(float value)
    {
    	int combination=7;
        if(!panel_passed[2])
        {
            my_player_script_3.setDigit3(value.ToString());  
            // compares to find when the values equal
            if (value == combination && !time_flag[2])
            {
                start_time[2] = Time.time;
                time_flag[2] = true;


            }
            else if (value != combination)
            {
                time_flag[2] = false; 

            }
            if (time_flag[2])
            {
                double curr_time = Time.time;

                // IMU was held accordingly to the combination
                if((curr_time-start_time[2]) > passed_time )
                {
                    // increase level
                    //curr_level = 4; 



                    time_flag[2] = false;
                    panel_passed[2] = true;
                }
            }
        }
        //do nothing
        else{}
    }

     // Level 4 Execution
    void level_4(float value)
    {
    	int combination=3;
        if (!panel_passed[3])
        {
        	Debug.Log("sjkhgilae");
            my_player_script_4.setDigit4(value.ToString());  
            // compares to find when the values equal
            if (value == combination && !time_flag[3])
            {
                start_time[3] = Time.time;
                time_flag[3] = true;

            }
            else if (value != combination)
            {
                time_flag[3] = false; 

            }
            if (time_flag[3])
            {
                double curr_time = Time.time;

                // IMU was held accordingly to the combination
                if((curr_time-start_time[3]) > passed_time )
                {
                    // increase level
                    //curr_level = 5; 


                    time_flag[3] = false;
                    panel_passed[3] = true; 
                }
            }
        }
        //do nothing
        else{}
    }
}
    