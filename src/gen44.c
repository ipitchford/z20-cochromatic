/* Orderly generation of ALL (4,4)-Ramsey graphs (K4-free AND independent-4-set-free)
 * up to isomorphism, level by level, using nauty for canonical forms.
 *
 * Purpose: independently confirm that there are EXACTLY TWO (4,4,16) graphs,
 * removing the last external dependency (McKay's catalogue completeness) from
 * the z(20)=6 proof.  Also re-derives R(4,4)=18 as a by-product (level 18 empty).
 *
 * Completeness argument: every induced subgraph of a (4,4)-graph is a (4,4)-graph,
 * so every (4,4,n+1) graph arises from SOME (4,4,n) graph by adding one vertex.
 * Extending every level-n class by every admissible neighbourhood therefore
 * reaches every level-(n+1) class.
 *
 * Admissibility: adding v with N(v)=S keeps the graph hom4-free iff
 *    G[S]    contains no triangle          (else v + triangle = K4)
 *    G[V\S]  contains no independent triple (else v + ind. triple = indep 4-set)
 * With alpha(G)<=3, omega(G)<=3 and R(3,4)=9 this forces n-8 <= |S| <= 8.
 */
#define MAXN 32
#include "nauty.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define KW 3                      /* 3 x uint64 = 192 bits of packed upper triangle */

static int N;                     /* size of graphs at the CURRENT level */
static unsigned int adj[MAXN];    /* working adjacency (bitmask per vertex) */

/* ---------------- storage for one level ---------------- */
typedef struct { unsigned long long *k; size_t cnt, cap; } Level;
static void lv_init(Level *L){ L->cnt=0; L->cap=1<<12; L->k=malloc(L->cap*KW*8); }
static void lv_push(Level *L, unsigned long long *key){
    if(L->cnt==L->cap){ L->cap*=2; L->k=realloc(L->k, L->cap*KW*8); }
    memcpy(L->k + L->cnt*KW, key, KW*8); L->cnt++;
}

/* ---------------- hash set over packed keys ---------------- */
static unsigned int *tab; static size_t tabsz, tabmask;
static Level *tabsrc;
static void tab_init(size_t n){
    tabsz=1; while(tabsz < n*2) tabsz<<=1; tabmask=tabsz-1;
    tab=malloc(tabsz*sizeof(unsigned int));
    for(size_t i=0;i<tabsz;i++) tab[i]=0xFFFFFFFFu;
}
static unsigned long long hashk(unsigned long long *k){
    unsigned long long h=1469598103934665603ULL;
    for(int i=0;i<KW;i++){ h^=k[i]; h*=1099511628211ULL; }
    return h;
}
static int tab_insert(unsigned long long *key){       /* 1 if new */
    size_t p=hashk(key)&tabmask;
    while(tab[p]!=0xFFFFFFFFu){
        if(!memcmp(tabsrc->k + (size_t)tab[p]*KW, key, KW*8)) return 0;
        p=(p+1)&tabmask;
    }
    tab[p]=(unsigned int)tabsrc->cnt;                  /* index of the graph we're about to push */
    return 1;
}

/* ---------------- nauty canonical form ---------------- */
static graph gg[MAXN*MAXM], cg[MAXN*MAXM];
static int lab[MAXN], ptn[MAXN], orbits[MAXN];
static DEFAULTOPTIONS_GRAPH(opts);
static statsblk stats;

static void canon_key(unsigned int *a, int n, unsigned long long *key){
    int m = SETWORDSNEEDED(n);
    EMPTYGRAPH(gg, m, n);
    for(int i=0;i<n;i++)
        for(int j=i+1;j<n;j++)
            if(a[i]>>j & 1u){ ADDONEEDGE(gg, i, j, m); }
    opts.getcanon = TRUE;
    densenauty(gg, lab, ptn, orbits, &opts, &stats, m, n, cg);
    /* pack canonical upper triangle */
    memset(key, 0, KW*8);
    int p=0;
    for(int j=1;j<n;j++)
        for(int i=0;i<j;i++){
            if(ISELEMENT(GRAPHROW(cg,i,m), j)) key[p>>6] |= 1ULL<<(p&63);
            p++;
        }
}
static void unpack(unsigned long long *key, int n, unsigned int *a){
    for(int i=0;i<n;i++) a[i]=0;
    int p=0;
    for(int j=1;j<n;j++)
        for(int i=0;i<j;i++){
            if(key[p>>6]>>(p&63) & 1ULL){ a[i]|=1u<<j; a[j]|=1u<<i; }
            p++;
        }
}

/* ---------------- admissibility tests ---------------- */
static int has_indep_triple(unsigned int *a, unsigned int C, int n){
    for(int i=0;i<n;i++){ if(!(C>>i&1u)) continue;
        unsigned int ci = C & ~a[i] & ~((1u<<(i+1))-1);
        for(int j=i+1;j<n;j++){ if(!(ci>>j&1u)) continue;
            unsigned int cj = ci & ~a[j] & ~((1u<<(j+1))-1);
            if(cj) return 1;
        }
    }
    return 0;
}

static Level *NEXT; static int NN;                 /* target level size = N+1 */
static unsigned int *CA;                           /* current graph adjacency */
static unsigned long long tmpkey[KW];
static unsigned int newadj[MAXN];

static void emit(unsigned int S){
    unsigned int full = (N==32)?0xFFFFFFFFu:((1u<<N)-1);
    if(has_indep_triple(CA, full & ~S, N)) return;
    for(int i=0;i<N;i++) newadj[i]=CA[i];
    newadj[N]=S;
    for(int i=0;i<N;i++) if(S>>i&1u) newadj[i] |= 1u<<N;
    canon_key(newadj, NN, tmpkey);
    if(tab_insert(tmpkey)) lv_push(NEXT, tmpkey);
}

static void rec(int start, unsigned int S, int size, int lo){
    if(size>=lo) emit(S);
    if(size==8) return;
    for(int v=start; v<N; v++){
        if(N - v + size < lo) break;               /* cannot still reach lo */
        unsigned int nb = CA[v] & S;               /* neighbours of v already in S */
        int tri=0;
        for(int u=0; u<N && !tri; u++) if(nb>>u&1u) if(CA[u]&nb) tri=1;
        if(!tri) rec(v+1, S | (1u<<v), size+1, lo);
    }
}

int main(int argc, char**argv){
    int LIMIT = (argc>1)? atoi(argv[1]) : 18;
    Level cur, nxt;
    lv_init(&cur);
    unsigned long long k0[KW]; memset(k0,0,sizeof k0);
    lv_push(&cur, k0);                              /* n = 1 : single vertex */
    N = 1;
    printf("n= 1: %zu\n", cur.cnt); fflush(stdout);

    while(N < LIMIT){
        NN = N+1;
        lv_init(&nxt);
        NEXT = &nxt; tabsrc = &nxt;
        tab_init(cur.cnt*8 + 1024);
        int lo = (N-8 > 0) ? N-8 : 0;
        for(size_t g=0; g<cur.cnt; g++){
            unpack(cur.k + g*KW, N, adj);
            CA = adj;
            rec(0, 0u, 0, lo);
        }
        free(tab);
        free(cur.k);
        cur = nxt; N = NN;
        printf("n=%2d: %zu\n", N, cur.cnt); fflush(stdout);
        if(cur.cnt==0){ printf("R(4,4) = %d  (no (4,4)-graph on %d vertices)\n", N, N); break; }
        if(N>=15){
            for(size_t g=0; g<cur.cnt; g++){
                unsigned int a[MAXN]; unpack(cur.k+g*KW, N, a);
                /* graph6 */
                char s[64]; int p=0; s[p++]=(char)(N+63);
                int bits[256], nb2=0;
                for(int j=1;j<N;j++) for(int i=0;i<j;i++) bits[nb2++] = (a[i]>>j)&1u;
                for(int t=0;t<nb2;t+=6){ int v=0; for(int b=0;b<6;b++) v=(v<<1)|((t+b<nb2)?bits[t+b]:0); s[p++]=(char)(v+63); }
                s[p]=0; printf("     %s\n", s);
            }
            fflush(stdout);
        }
    }
    return 0;
}
