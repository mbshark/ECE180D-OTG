using UnityEngine;
using System.Collections;
using System.Net.Sockets;
using System.Collections.Generic;
using System;
using System.Net;
using System.io;

public class Server : MonoBehavior
{
	private List<ServerClient> clients;
	private List<ServerClient> disconnectList;

	public int port = 8888;

	private TcpListener server;
	private bool serverStarted;

	private void Start()
	{
		clients = new List<ServerClient>();
		disconnectList = new List<ServerClient>();

		try
		{
			server = new TcpListener(IPAddress.Any, port);
			server.start();

			StartListening(); 
			serverStarted = true;
			Debug.Log("Server Started")
		}
		catch(Exception e)
		{
			 Debug.Log("Socket Error: " + e.Message)
		}
	}

	private void Update()
	{
		if (!serverStarted)
		return;

		foreach (ServerClient c in clients)
		{
			if (isConnected(c.tcp))
			{
				c.tcp.Close();
				disconnectList.Add(c);
				continue;
			}
			else
			{
				NetworkStream s = c.tcp.GetStream();
				if (s.DataAvailable)
				{
					StreamReader reader = new StreamReader(s,true);
					string data = reader.ReadLine();

					if (data!= null)
					{
						OnIncomingData(c, data);
					}
				}
			}
		}
	}

	private void StartListening()
	{
		server.BeginAcceptTcpClient(AcceptTcpClient, server)
	}

	private bool isConnected(TcpClient c)
	{
		try 
		{
			if (c != null && c.Client !=null && c.Client.Connect)
			{
				if (c.Client.Poll(0, SelectMode.SelectRead))
				{
					return !(c.Client.Receive(new byte[1],SocketFlags.Peek) == 0)
				}
			}
			return true;
		}
		catch
		{
			return false;
		}
	}

	private void AcceptTcpClient(TAsyncResult ar)
	{
		TcpListener listener = (TcpListener)ar.AsyncState;

		clients.Add(new ServerClient(listener.EndAcceptTcpClient(ar)));
		StartListening();
	}

	private void OnIncomingData(ServerClient c, string data)
	{
		Debug.Log(c.clientName + " sent : " + data);
	}
}




public class ServerClient
{
	public TcpClient tcp;
	public string clientName;

	public ServerClient(TcpClient clientSocket)
	{
		clientName = "Guest";
		tcp = clientSocket;
	}
}

public static void Main(string[] args)
{
	Console.WriteLine("Criminininalalal")
}