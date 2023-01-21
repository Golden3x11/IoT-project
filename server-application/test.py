from service import handle_ticket_usage
import database_conn as db

db.init_database()
handle_ticket_usage("orzel1")
handle_ticket_usage("orzel2")
handle_ticket_usage("orzel3")
handle_ticket_usage("orzel4")
handle_ticket_usage("orzel5")
handle_ticket_usage("orzel1")
handle_ticket_usage("orzel2")
handle_ticket_usage("orzel3")
handle_ticket_usage("orzel4")
handle_ticket_usage("orzel5")
handle_ticket_usage("orzel3")
handle_ticket_usage("orzel4")
handle_ticket_usage("orzel5")