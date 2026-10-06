CREATE TABLE IF NOT EXISTS events(
event_id TEXT PRIMARY KEY,event_type TEXT NOT NULL,ts TEXT NOT NULL,site TEXT NOT NULL,lp TEXT,
session_id TEXT NOT NULL,page_id TEXT NOT NULL,path TEXT NOT NULL,title TEXT,referrer TEXT,
utm_source TEXT,utm_medium TEXT,utm_campaign TEXT,utm_term TEXT,utm_content TEXT,gclid TEXT,
campaign_id TEXT,adgroup_id TEXT,keyword TEXT,matchtype TEXT,device TEXT,network TEXT,creative TEXT,
selector TEXT,label TEXT,section TEXT,x_norm REAL,y_norm REAL,depth INTEGER,active_ms INTEGER,elapsed_ms INTEGER,meta_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_events_site_ts ON events(site,ts);
CREATE INDEX IF NOT EXISTS idx_events_lp_ts ON events(lp,ts);
CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id,ts);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type,ts);
CREATE INDEX IF NOT EXISTS idx_events_keyword ON events(keyword,ts);