import json
from flask import Flask, jsonify

app = Flask(__name__)

with open(r'notifications-feed.json', 'r') as file:
    notifications_feed = json.load(file)


# Aggregation function
def aggregate_notifications(notifications):
    
    aggregated_data = {}
    
    for notification in notifications:
        post_id = notification['post']['id']
        notification_type = notification['type']
        user_name = notification['user']['name']
        
        # Initialize if post_id not in aggregated_data
        if post_id not in aggregated_data:
            aggregated_data[post_id] = {
                'title': notification['post']['title'], 
                'Like': {
                    'count': 0,
                    'names': []
                    }, 
                'Comment': {
                    'count': 0,
                    'names': [],
                    'details': {}
                    }
                }
        
        # Increment counts based on notification type
        if notification_type == 'Like':
            aggregated_data[post_id]['Like']['count'] += 1
            aggregated_data[post_id]['Like']['names'].append(user_name)
        elif notification_type == 'Comment':
            aggregated_data[post_id]['Comment']['count'] += 1
            aggregated_data[post_id]['Comment']['details'][user_name] = notification['comment']['commentText']  
            aggregated_data[post_id]['Comment']['names'].append(user_name)
        
    return aggregated_data


aggregated_notifications = aggregate_notifications(notifications_feed)

# Endpoint to retrieve aggregated data
@app.route('/notifications', methods=['GET'])
def get_aggregated_notifications():
    return jsonify(aggregated_notifications)

if __name__ == '__main__':
    app.run(debug=True)
