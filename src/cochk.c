/* Read graph6 graphs from stdin; report any that are NOT k-cocolourable.
 * (k-cocolourable = V partitions into at most k classes, each a clique or an
 * independent set.)  Usage:  ./cochk <k>
 *
 * Used to verify:
 *   z(8) <= 3 :  geng -q 8       | ./cochk 3     (all 12346 graphs on 8 vertices)
 *   z(12)<= 4 :  gen44 -d12      | ./cochk 4     (all (4,4,12) graphs)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int N;
static unsigned int adj[32];

static int ctz(unsigned int x){ int c=0; while(!(x&1u)){x>>=1;c++;} return c; }
static int pc(unsigned int x){ int c=0; while(x){x&=x-1;c++;} return c; }

static int can(unsigned int mask, int k);

/* enumerate homogeneous blocks B (clique or independent) with v = min(mask),
 * B subset of mask, then recurse. */
static int try_blocks(unsigned int mask, int k, unsigned int B,
                      unsigned int cand, int clique){
    if(can(mask ^ B, k-1)) return 1;                /* B complete as-is */
    unsigned int c = cand;
    while(c){
        unsigned int bit = c & (~c + 1u);
        int u = ctz(bit);
        c ^= bit;
        unsigned int nc = clique ? (cand & adj[u]) : (cand & ~adj[u]);
        nc &= ~((bit<<1) - 1u);                     /* only higher-indexed, avoid repeats */
        if(try_blocks(mask, k, B | bit, nc, clique)) return 1;
    }
    return 0;
}

static int can(unsigned int mask, int k){
    if(mask == 0) return 1;
    if(k == 0) return 0;
    if(pc(mask) > k * N) return 0;
    unsigned int vb = mask & (~mask + 1u);
    int v = ctz(vb);
    unsigned int rest = mask & ~vb & ~((vb<<1) - 1u);
    /* cliques containing v */
    if(try_blocks(mask, k, vb, rest & adj[v], 1)) return 1;
    /* independent sets containing v */
    if(try_blocks(mask, k, vb, rest & ~adj[v], 0)) return 1;
    return 0;
}

int main(int argc, char**argv){
    int k = (argc>1) ? atoi(argv[1]) : 4;
    char line[512];
    long long total=0, bad=0;
    while(fgets(line, sizeof line, stdin)){
        int len = (int)strlen(line);
        while(len>0 && (line[len-1]=='\n' || line[len-1]=='\r')) line[--len]=0;
        if(len==0) continue;
        N = line[0] - 63;
        if(N < 1 || N > 31) continue;
        for(int i=0;i<N;i++) adj[i]=0;
        int p=1, bitpos=0, nbits=N*(N-1)/2;
        int val=0, have=0;
        for(int idx=0; idx<nbits; idx++){
            if(have==0){ val = line[p++] - 63; have = 6; }
            int b = (val >> (have-1)) & 1; have--;
            /* graph6 order: for j=1..N-1, for i=0..j-1 */
            int j=1, i=0, t=idx;
            while(t >= j){ t -= j; j++; }
            i = t;
            if(b){ adj[i] |= 1u<<j; adj[j] |= 1u<<i; }
            bitpos++;
        }
        total++;
        unsigned int full = (N==32)?0xFFFFFFFFu:((1u<<N)-1);
        if(!can(full, k)){
            bad++;
            printf("NOT %d-cocolourable: %s\n", k, line);
            if(bad > 20){ printf("...more than 20 failures, stopping\n"); break; }
        }
        if(total % 200000 == 0){ fprintf(stderr, "  ...%lld checked, %lld bad\n", total, bad); fflush(stderr); }
    }
    printf("checked %lld graphs; %lld NOT %d-cocolourable\n", total, bad, k);
    return bad ? 1 : 0;
}
