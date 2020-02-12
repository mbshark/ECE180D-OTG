using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class decreasing : MonoBehaviour
{

    private int level = 5;
    public Text level_text;
    private string roll = null;
    private string pitch = null; 



    // Use this for initialization

    void Start()
    {
        // Usually the server doesn't need to draw anything on the screen
        Thread thr2 = new Thread(CreateServer);
        thr2.Start();
    }

        

        
    void CreateServer()
    {
        IPHostEntry ipHost = Dns.GetHostEntry(Dns.GetHostName());
        //GetHostName not working on mac
        // Debug.Log(ipHost.AddressList[3]);
        IPAddress ipAddr = ipHost.AddressList[3];

        IPEndPoint localEndPoint = new IPEndPoint(ipAddr, 5005);

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
                Socket clientSocket = listener.Accept();

                // Data buffer 
                byte[] bytes = new Byte[1024];

                while (true)
                {
                    int numByte = clientSocket.Receive(bytes);

                    string data = Encoding.ASCII.GetString(bytes,
                                               0, numByte);
                    if (data[0] == 'I'){
	                    string[] words = data.Split(',');
	                    roll = words[1];
	                    pitch = words[2];

	                    if (data.IndexOf("#") > -1)
	                    {
	                        Debug.Log("failed");
	                        break;
	                    }
	                } else if (data[0] == 'S'){
	                	Debug.Log(data)
	                	cmd = data[1:]
	                	Debug.Log(cmd)
	                	msg = "";
	                	if (cmd.Equals("hint")){
	                		msg = "Here is a very useful hint";
	                	} else if (cmd.Equals("play")) {
	                		msg = "Resume the game";
						} else if (cmd.Equals("pause")){
							msg = "Game is now PAUSED;"
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

    


    void Update()
    {
        level_text.text = "Roll: " +roll+"\n"+"Pitch: "+pitch;   
    }

}