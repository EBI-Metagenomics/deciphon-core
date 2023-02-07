struct dcp_press;
struct dcp_scan;

struct dcp_press *dcp_press_new(void);
int dcp_press_open(struct dcp_press *, char const *hmm, char const *db);
long dcp_press_nproteins(struct dcp_press const *);
int dcp_press_next(struct dcp_press *);
bool dcp_press_end(struct dcp_press const *);
int dcp_press_close(struct dcp_press *);
void dcp_press_del(struct dcp_press const *);

struct dcp_scan *dcp_scan_new(int port);
void dcp_scan_del(struct dcp_scan const *);

int dcp_scan_set_nthreads(struct dcp_scan *, int nthreads);
void dcp_scan_set_lrt_threshold(struct dcp_scan *, double);
void dcp_scan_set_multi_hits(struct dcp_scan *, bool);
void dcp_scan_set_hmmer3_compat(struct dcp_scan *, bool);

int dcp_scan_set_db_file(struct dcp_scan *, char const *db);
int dcp_scan_set_seq_file(struct dcp_scan *, char const *seqs);

int dcp_scan_run(struct dcp_scan *, char const *name);

char const *dcp_strerror(int err);
