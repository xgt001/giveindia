package com.facebook.client;

//Different packages that are been used
import java.util.ArrayList;
import org.json.JSONArray;
import org.json.JSONObject;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.widget.TextView;

import com.facebook.*;
import com.facebook.android.R;
import com.facebook.model.GraphObject;
import com.facebook.model.GraphUser;


public class FirstApp extends FragmentActivity
{
	//The different queries that are run
	private ArrayList<String> queries = new ArrayList<String>();
	private static ArrayList<String> getAndGenerateQueries(ArrayList<String> q)
	{
		//q.add("select fan_count, username from page where username = \"teachforindia\"");
		//q.add("select uid from page_fan where page_id in (select page_id from page where username = 'teachforindia') and uid in ( select uid2 from friend where uid1 = me())");
		//q.add("select uid from page_fan where page_id = '104779413448 and uid = 529770637 ");
		q.add("select current_location, hometown_location from user where uid = me()");
		q.add("select fan_count from page where username = \"giveIndia\"");
		return q;
	}
	
	
	@Override
	protected void onCreate(Bundle savedInstanceState) 
	{
		super.onCreate(savedInstanceState);
		setContentView(R.layout.myapp);
		//The active session is retrieved and the processing is done
		Session.openActiveSession(this, true, new Session.StatusCallback() {
			
			@Override
			public void call(final Session session, SessionState state, Exception exception) {
				// TODO Auto-generated method stub
				if(session.isOpened())//if session is open
				{
					//Request to the facebook server for the current session
					Request.executeMeRequestAsync(session, new Request.GraphUserCallback() 
					{
						@Override //Once the user is authenticated correctly
						public void onCompleted(GraphUser user, Response response)
						{
							// TODO Auto-generated method stub
							if(user != null)
							{
								String usrname = user.getUsername();//Username of the logged in user is fetched
								final TextView w = (TextView) findViewById(R.id.textView2);
								TextView w2 = (TextView) findViewById(R.id.textView1);
							
									w2.setText("Welcome " + usrname + "!\n"); //The user is welcomed
									queries = getAndGenerateQueries(queries);
									
									for(String query : queries)//for different queries
									{	
										//Fill the Request object to be sent the fql database over the Http server
									    Bundle params = new Bundle();
									    params.putString("q", query);
									    Session session = Session.getActiveSession();
									    Request request = new Request(session, "/fql", params, HttpMethod.GET, new Request.Callback()
									    {         
									           public void onCompleted(Response response)
									           {
									        	   	//The JSON object is returned by the fql database
									        	   	GraphObject go = response.getGraphObject();
									        	   	try
									        	   	{
									        	   		//It is parsed, the latitude and the longitude are fetched.
									        	   		JSONArray json_obj = go.getInnerJSONObject().getJSONArray("data");
									        	   		JSONObject jsobj = json_obj.getJSONObject(0);
									        	   		String lat1 = jsobj.getJSONObject("current_location").getString("latitude");
									        	   		String lon1 = jsobj.getJSONObject("current_location").getString("longitude");
									        	   		String city1 = jsobj.getJSONObject("current_location").getString("city");
									        	   		String lat2 = jsobj.getJSONObject("hometown_location").getString("latitude");
									        	   		String lon2 = jsobj.getJSONObject("hometown_location").getString("longitude");
									        	   		String city2 = jsobj.getJSONObject("hometown_location").getString("city");
									        	   		
									                    w.setText("Current City:\n" + city1 + "\n" + lat1 + "\n" + lon1 + "\nHometown:\n" + city2 + "\n" + lat2 + "\n" + lon2);
									        	   	}
									        	   	catch(Exception e)
									        	   	{
									        	   		
									        	   	}
									        	   	}
									            }                  
									    ); 
									    Request.executeBatchAsync(request);
									}
								}
							}
						}
					);
				}
			}
		
		});
	}
	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) 
	{
		super.onActivityResult(requestCode, resultCode, data);
		Session.getActiveSession().onActivityResult(this, requestCode, resultCode, data);
	}
}
