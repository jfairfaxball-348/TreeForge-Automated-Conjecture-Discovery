# TF22 — the unique-empty hub as a global extremal obstruction

Date: 2026-10-04

For a finite tree \(T\), write

\[
\zeta(T)=\#\{D\subseteq V(T):D\text{ is a minimum dominating set of }T\}
\]

and

\[
M_n=\max\{\zeta(T):T\text{ is a tree of order }n\}.
\]

TF22 attacks only the unique-empty no-universal class left by TF21, while
keeping TF20's residual strong-banked class separate. No order at least 15 is
generated or inspected.

**Decision.** TF22 finds a real global structure theorem, but not the missing
extremal closure. The TF21 deletion components are exactly the nontrivial
\(\gamma\)-excellent trees of the domination literature, and the attachment
vertices are exactly stable vertices in those components. Hence the entire
unique-empty class has a published recursive *shape* grammar. However the
exact hub objective is intrinsically two-dimensional. Context-universal
same-order replacement is governed by the pair
\((\zeta(R),\alpha_r)\), where \(\alpha_r\) counts component \(\gamma\)-sets
containing the root. Taletskii's \(W_{a,b}\) family gives an analytic
infinite family in which balancing improves the first coordinate while
worsening the second, and legitimate flexible outside contexts reverse which
choice is better. A path family also proves that rerooting at a critical
vertex can strictly *decrease* the full hub objective. Thus the natural
rerooting, equal-order dominance, balancing, and cross-component replacement
routes do not collapse the class to a context-free finite menu.

The residual strong-banked class is still not globally excluded either.
Consequently TF22 does not derive \(M_{15}\), freezes no experiment, and
formally pauses the unrestricted multiplicity programme at this
replacement-theoretic endpoint.

## 1. Provenance and scientific boundary

TF22 starts from exact merged `main`

`1c6445b61c137d775c306452bc0b817c4dcca4b4`.

The requested TF21 provenance verifies exactly:

- TF21 PR #27 exact head:
  `f93fa0b868fa061cd2cf062e736c885aec3bae8b`;
- exact-head Actions run `37209711381`: completed successfully;
- TF21 merge / TF22 starting main:
  `1c6445b61c137d775c306452bc0b817c4dcca4b4`;
- post-merge Actions run `37209936379`: completed successfully.

Both green runs completed installation, the full unit suite, byte-compilation,
Ruff static analysis, deterministic calibration, all historical deterministic
diagnoses, TF20 global compensation, and TF21 one-vertex compensation.

PR #27 changed exactly:

- `.github/workflows/ci.yml`;
- `HANDOVER.md`;
- `README.md`;
- `ROADMAP.md`;
- `docs/FAILURE_AND_LESSON_LEDGER.md`;
- `docs/TF21_ONE_VERTEX_COMPENSATION.md`;
- `experiments/tf21_one_vertex_compensation_diagnosis.py`;
- `tests/test_tf21_one_vertex_compensation_diagnosis.py`.

The live boundary also verifies:

- the permanent candidate history reaches `TF-001157` and
  `TF-001158` remains next;
- the last scientific experiment remains `TF4-0001`;
- `minimum_dominating_set_count` remains non-default theorem/diagnostic
  machinery;
- the default invariant registry is unchanged;
- orders 1--14 remain the burned diagnostic universe;
- orders 15 and above remain untouched.

The candidate JSONL is large; a connector preview initially displayed it as
empty, but direct repository-content inspection shows 3,699 revision rows and
maximum permanent ID `TF-001157`. This was a read-size artefact, not a
repository discrepancy.

## 2. The TF21 residue, stated as the TF22 input theorem

Let \(T\) be an exact order-extremizer with no universal vertices.

TF21 proves that \(T\) has at most one empty vertex. If it has exactly one,
call it \(u\). Then

\[
T-u=T_1\cup\cdots\cup T_k,\qquad k\ge2,
\]

where \(r_i\) is the neighbour of \(u\) in \(T_i\). Every vertex of every
\(T_i\) is flexible, and

\[
\gamma(T)=\sum_i\gamma(T_i).
\]

Write the exact root states at \(r_i\) as

\[
A_i=(\gamma_i,\alpha_i),\qquad
B_i=(\gamma_i,\beta_i),\qquad
C_i=(c_i,\chi_i),
\]

with an infeasible \(C_i\) allowed. Then

\[
c_i\ge\gamma_i
\]

at every actual TF21 attachment root and

\[
\boxed{\;
\zeta(T)=
\prod_i(\alpha_i+\beta_i)-\prod_i\beta_i.
\;}
\]

This statement, rather than the infinite TF19 local context quotient, is the
formal input object for TF22.

## 3. Literature terminology: all-flexible means nontrivial \(\gamma\)-excellent for trees

Burton and Sumner define a vertex to be \(\gamma\)-good if it belongs to some
minimum dominating set, and a graph to be \(\gamma\)-excellent if every
vertex is \(\gamma\)-good. For trees on at least four vertices they prove
that \(\gamma\)-excellent, dot-critical, critically dominated, and crucially
dominated are equivalent, and give a constructive characterization.

They also classify a vertex \(v\) by the change in domination number after
deletion:

- **critical:** \(\gamma(T-v)=\gamma(T)-1\);
- **stable:** \(\gamma(T-v)=\gamma(T)\);
- **nova:** \(\gamma(T-v)=\gamma(T)+1\).

For trees, a vertex is nova if and only if it belongs to every minimum
dominating set.

Samodivkin's later terminology is also useful:

- \(\gamma\)-fixed: in every \(\gamma\)-set;
- \(\gamma\)-free: in some but not all \(\gamma\)-sets;
- \(\gamma\)-bad: in no \(\gamma\)-set.

Thus TreeForge's **flexible** is exactly \(\gamma\)-free.

### Theorem 3.1 — all-flexible tree characterization

A nontrivial tree \(R\) is all-flexible if and only if it is
\(\gamma\)-excellent.

More precisely, \(K_2\) is all-flexible; \(K_1\) is \(\gamma\)-excellent but
its sole vertex is universal; and there is no \(\gamma\)-excellent tree of
order three.

**Proof.** If every vertex is flexible, every vertex occurs in some
\(\gamma\)-set, so \(R\) is \(\gamma\)-excellent.

Conversely, let \(R\) be a \(\gamma\)-excellent tree of order at least four.
A critical vertex is \(\gamma\)-good and is also omitted by a \(\gamma\)-set:
take a \((\gamma(R)-1)\)-set of \(R-v\) and add a neighbour of \(v\).
Every noncritical vertex of a \(\gamma\)-excellent tree is stable by
Burton--Sumner, hence not nova; for trees nova is equivalent to belonging to
every \(\gamma\)-set. Therefore every vertex occurs in some but not all
\(\gamma\)-sets. The \(K_2\) case is immediate. \(\square\)

So TF21's deletion components are not a new unnamed class. They are exactly
the nontrivial \(\gamma\)-excellent trees.

### Published constructive grammars

Burton--Sumner prove that a \(\gamma\)-excellent tree is \(K_1\), \(K_2\),
or is obtained from \(K_1\) by repeatedly appending:

1. a 2-attachment at a noncritical/stable vertex; or
2. a 3-attachment at a critical vertex.

Samodivkin gives a useful reformulation for trees of order at least four:
start from a labeled 1-corona tree and repeatedly coalesce another labeled
1-corona at a critical vertex. The resulting labels satisfy

\[
0_T=V^-(T),\qquad 1_T=V^=(T),
\]

so label 0 means critical and label 1 means stable.

This is a complete recursive **shape** grammar. It is not yet an extremal
grammar for \(\zeta\): the exact rooted counts carried by the blocks are
unbounded.

## 4. Criticality is exactly the cheap-\(C\) state

The literature classification has a direct TF17 state interpretation.

### Lemma 4.1

Let \(R\) be a tree, let \(r\) be flexible, and write
\(\gamma=\gamma(R)\). Then

\[
r\text{ is critical}
\quad\Longleftrightarrow\quad
\operatorname{cost}(C_r)=\gamma-1.
\]

**Proof.** A feasible \(C_r\)-configuration of cost \(\gamma-1\) dominates
\(R-r\), so \(r\) is critical.

Conversely, suppose \(r\) is critical and let \(D\) be a minimum dominating
set of \(R-r\), of size \(\gamma-1\). No neighbour of \(r\) can lie in
\(D\), otherwise \(D\) would dominate \(R\) itself with fewer than
\(\gamma\) vertices. Hence \(D\) is exactly a feasible \(C_r\)-configuration
of cost \(\gamma-1\). \(\square\)

### Corollary 4.2 — TF21 attachment roots are stable

Every actual root \(r_i\) in a unique-empty TF21 component is stable.

TF21 gives \(c_i\ge\gamma_i\); Lemma 4.1 says a critical root would have
\(c_i=\gamma_i-1\).

This is the first genuinely new global restriction beyond “all vertices are
flexible.”

## 5. Complete structural grammar of the unique-empty class

The previous results have a converse.

### Theorem 5.1 — stable-root \(\gamma\)-excellent hub theorem

A tree has no universal vertices and exactly one empty vertex \(u\) if and
only if it can be obtained as follows:

1. take \(k\ge2\) vertex-disjoint nontrivial \(\gamma\)-excellent trees
   \(R_1,\ldots,R_k\);
2. choose a stable vertex \(r_i\in V(R_i)\) in each;
3. add one new vertex \(u\) and the edges \(ur_i\).

For this tree,

\[
\gamma(T)=\sum_i\gamma(R_i)
\]

and, writing

\[
s_i=\zeta(R_i)=\alpha_i+\beta_i,
\]

\[
\boxed{\;
\zeta(T)=\prod_i s_i-\prod_i\beta_i.
\;}
\]

**Proof.** The forward direction is TF21, Theorem 3.1, and Corollary 4.2.

For the converse, all roots have \(A_i=B_i=\gamma_i\) and no root has a
cheaper \(C_i\). Therefore at \(u\), the unselected-and-dominated state has
cost \(\sum\gamma_i\), while the selected state costs at least one more.
Thus \(u\) is empty and the displayed product-minus-product formula follows.

Every component vertex remains flexible. To realize a \(\gamma\)-set
containing or omitting a chosen component vertex, choose the corresponding
component \(\gamma\)-set; if that choice does not select its attachment root,
use another component (possible because \(k\ge2\)) and a \(\gamma\)-set
containing that component's root to dominate \(u\). Hence \(u\) is the only
empty vertex and there is no universal vertex. \(\square\)

This completely classifies the **shape** of the unique-empty class. It does
not classify which such trees can maximize \(\zeta\) at a fixed order.

## 6. Full rerooting accounting

Rerooting a component need not stay inside the unique-empty class.

For an arbitrary flexible root let \(t\) be the number of component roots
that are critical. Put \(G=\sum_i\gamma_i\). At the hub,

\[
\operatorname{cost}(B_u)=G
\]

and

\[
\operatorname{cost}(A_u)=1+G-t.
\]

Therefore:

- \(t=0\): \(u\) is empty;
- \(t=1\): \(u\) is flexible;
- \(t\ge2\): \(u\) is universal.

If exactly one root \(r_j\) is critical, let
\(C_j=(\gamma_j-1,\chi_j)\), and for each other component set

\[
m_i=
\begin{cases}
s_i+\chi_i,&c_i=\gamma_i,\\
s_i,&c_i>\gamma_i\text{ or }C_i\text{ infeasible}.
\end{cases}
\]

Then the selected-hub minimum sets contribute exactly

\[
\chi_j\prod_{i\ne j}m_i.
\]

So a move to a critical root is not a small perturbation of \(\beta\): it
changes which hub state is optimal.

### Stable-root rerooting theorem

If a component \(R\) is rerooted from one stable vertex \(r\) to another
stable vertex \(s\), all other components fixed, then

\[
Z_s-Z_r=
\Bigl(\prod_{i\ne R}\beta_i\Bigr)(\beta_r-\beta_s).
\]

Equivalently an extremal unique-empty hub must attach each component at a
stable vertex minimizing \(\beta\), or equivalently maximizing \(\alpha\).

This is exact but does not classify the stable optimum.

### Critical rerooting is not monotone

Suppose only component \(R\) is moved from stable \(r\) to critical \(c\).
Let \(C_c=(\gamma(R)-1,\chi_c)\). With

\[
B=\prod_{\text{other }i}\beta_i,\qquad
M=\prod_{\text{other }i}m_i,
\]

the exact change is

\[
\boxed{\;
\Delta Z=(\beta_r-\beta_c)B+\chi_c M.
\;}
\]

The sign depends on the whole outside context.

There is an analytic negative family. For \(P_{3m+1}\), \(m\ge2\), a
standard gap count for minimum dominating sets gives

\[
\gamma=m+1,\qquad
\zeta=\frac{m^2+5m+2}{2}.
\]

Root at path vertex 2. It is stable and

\[
\beta_2=m+1.
\]

Path vertex 4 is critical and

\[
\beta_4=\frac{m^2+m+2}{2},\qquad \chi_4=1.
\]

With a single \(P_2\) as the other component, \(B=1\) and \(M=2\), so

\[
\Delta Z=
\frac{-m^2+m+4}{2}<0
\qquad(m\ge3).
\]

Thus “reattach the hub at a critical vertex so that selecting the hub becomes
competitive” is false even on the elementary all-flexible path family.

For completeness, the path count follows by encoding a minimum dominating
set of \(P_{3m+1}\) by the unselected gaps before, between, and after its
\(m+1\) selected vertices. Relative to maximum allowed gaps, the total
defect is two. It can be one interior defect of size two, or two defects of
size one, giving

\[
m+\binom{m+2}{2}
=
\frac{m^2+5m+2}{2}.
\]

Conditioning on omission of vertex 2 and on inclusion of vertex 4 gives the
displayed root counts.

## 7. The exact equal-order component preorder

Fix every component except one rooted component \(R\). Let

\[
s=\zeta(R),\qquad
\alpha=\#\{\gamma\text{-sets containing }r\},\qquad
\beta=s-\alpha.
\]

For the outside components put

\[
A=\prod_{\mathrm{outside}}s_i,\qquad
B=\prod_{\mathrm{outside}}\beta_i.
\]

Because every outside root is flexible,

\[
A>B>0.
\]

Then

\[
\boxed{\;
Z=A s-B\beta=(A-B)s+B\alpha.
\;}
\]

This is the natural coordinate system. The objective is a positive linear
functional of \((s,\alpha)\).

### Theorem 7.1 — context-universal component dominance

For two equal-order all-flexible components with stable roots,
\(R=(s,\alpha)\) and \(R'=(s',\alpha')\), replacement \(R\to R'\) never
decreases the unique-empty hub objective in **every** valid outside context
if and only if

\[
s'\ge s,\qquad \alpha'\ge\alpha.
\]

It is strictly improving in every context when at least one inequality is
strict.

Sufficiency is immediate from the positive-linear formula. Necessity is
also exact. If \(s'<s\), use arbitrarily many \(P_2\) outside components:
then \(B/(A-B)=1/(2^k-1)\to0\), so the \(s\)-loss eventually dominates.
If \(\alpha'<\alpha\), use one \(P_{3m+1}\) rooted at path vertex 3.
That stable root has

\[
\alpha=2,\qquad\beta=\zeta-2,
\]

so \(B/(A-B)=(\zeta-2)/2\to\infty\); the \(\alpha\)-loss eventually
dominates.

Therefore \(\zeta\) alone, \(\beta\) alone, or any fixed scalar ratio cannot
be a context-universal replacement coordinate.

## 8. Cross-component exchange has the same obstruction

For two components set

\[
S=s_i s_j,\qquad
P=\beta_i\beta_j,\qquad
Q=S-P.
\]

With all other components fixed,

\[
Z=A S-BP=(A-B)S+BQ.
\]

Hence a pair replacement that is guaranteed not to lose in **every** outside
context must satisfy

\[
S'\ge S,\qquad Q'\ge Q,
\]

and these conditions are sufficient. The same \(P_2\) and
\(P_{3m+1}\) outside families show necessity.

So redistributing vertices between two components does not remove the
two-dimensional issue; it merely changes the two coordinates from
\((s,\alpha)\) to \((S,Q)\).

## 9. Taletskii \(W_{a,b}\): exact context reversal of balancing

Let \(W_{a,b}\) consist of a central path \(x-y-z\), with \(a\) disjoint
support/leaf arms at \(x\) and \(b\) at \(z\), where \(a,b\ge1\).

Every \(W_{a,b}\) is all-flexible. A direct count according to whether the
chosen central-path vertex is \(x,y,\) or \(z\) gives

\[
\zeta(W_{a,b})
=
3\cdot2^{a+b}-2^a-2^b.
\]

Root at a support on the \(a\)-side. The root is stable (indeed its
\(C\)-state is infeasible), and conditioning the same count on selecting the
root gives

\[
\alpha_{a,b}
=
3\cdot2^{a+b-1}-2^{a-1}.
\]

Now fix \(q\ge2\) and compare same-order components

\[
B_q=W_{q,q},
\qquad
U_q=W_{q-1,q+1},
\]

rooting \(U_q\) on the smaller side. Then

\[
\zeta(U_q)-\zeta(B_q)=-2^{q-1},
\]

but

\[
\alpha(U_q)-\alpha(B_q)=2^{q-2}.
\]

Thus balancing improves standalone multiplicity while making the rooted
inclusion coordinate worse.

The outside context decides which component is better.

- With one rooted \(P_2\), \(A=2,B=1\), so
  \(U_q-B_q=-2^{q-2}<0\): **balanced wins**.
- With one \(P_7\) rooted at path vertex 3, the exact root pair is
  \((s,\alpha,\beta)=(8,2,6)\), so \(A=8,B=6\), and
  \(U_q-B_q=2^{q-1}>0\): **unbalanced wins**.

Both outside roots are stable vertices of all-flexible trees. Hence both
are legitimate unique-empty hub contexts.

This is the sharpest TF22 obstruction. Even inside one explicit published
family, a same-order balancing move has no context-independent direction.
It also explains why the balanced-\(W\) competitor that defeats the
subdivided star as a whole tree cannot simply be promoted to a universal
component-balancing rule.

More generally, at fixed \(a+b=2q\), the rooted \(W_{a,2q-a}\) pairs for
\(1\le a\le q\) trade increasing \(\zeta\) against decreasing \(\alpha\).
The natural rooted family therefore contains arbitrarily long exact
two-coordinate antichains.

## 10. The subdivided-star obstruction remains canonical

For the subdivided \(k\)-arm star \(S_k\), every deletion component is a
\(P_2\) with

\[
(\alpha,\beta)=(1,1).
\]

Therefore

\[
\zeta(S_k)=2^k-1.
\]

TF21 already proves that, for \(k\ge3\), a balanced same-order
\(W_{a,b}\) tree with \(a+b=k-1\) has larger multiplicity. Hence
subdivided stars cease to be extremal after \(P_5=S_2\).

TF22 does not turn that one comparison into a component rule: Section 9
shows analytically that \(W\)-balancing itself reverses in legitimate hub
contexts.

\(P_5\) remains the exact order-5 unique-empty extremizer and therefore the
irreducible small exception to every universal one-vertex compensation
claim.

## 11. What the \(\gamma\)-excellent grammar does and does not buy

The Burton--Sumner and Samodivkin theorems answer a major TF22 structural
question positively:

- all-flexible components have a known recursive construction;
- every actual unique-empty attachment is at a stable vertex;
- in Samodivkin's labeled corona-block grammar, the hub attaches only to
  label-1 vertices.

The grammar nevertheless has unbounded geometry. A 1-corona of an
arbitrarily large star is all-flexible and has arbitrarily large degree.
Repeated critical coalescences also permit arbitrarily large block trees.

More importantly for the extremal objective, the exact stable-root count
pair \((\zeta,\alpha)\) is not collapsed by the grammar. The path and
\(W\)-families above give analytically unbounded and context-sensitive
values. A finite production alphabet is therefore not a finite-state
extremal recurrence.

This is why TF22 records the literature result as genuine global progress
without claiming that it solves \(M_n\).

## 12. Consequences for the no-empty side

If a no-universal exact extremizer has no empty vertices, TF20's use of
Taletskii's S-decomposition remains valid:

- every S-part has size at most three;
- adjacent support/preleaf separability remains available.

TF22 does not prove that every sufficiently large exact extremizer reaches
this side. The unique-empty class is now structurally characterized rather
than eliminated.

Accordingly bounded S-part size still cannot be promoted to a global
extremizer grammar.

## 13. Residual strong-banked class remains separate

TF20 proves that an exact extremizer with a strong support has:

- exactly one strong support \(v\);
- \(v\) as the unique universal vertex;
- exactly two private leaves at \(v\);
- those two leaves as its only empty neighbours.

TF21 proves that \(P_3\) prevents pairing those two empty leaves.

TF22 finds no theorem that excludes every nontrivial member of this class.
The exact accounting explains why the obvious moves remain insufficient.

If one private leaf is deleted, Taletskii gives the desired strict
multiplicity gain but again releases exactly one vertex. Reattaching that
leaf at \(v\) recreates the original tree and deletes the new
\(v\)-omitting minimum sets. Moving it elsewhere is not neutral in general.
Even among burned residual trees there are nontrivial examples where no
single relocation of that private leaf gives a strict improvement; this is a
diagnostic failure of the operation, not an extremality theorem.

Removing \(v\) and its two leaves does not reduce the remaining branches to
the unique-empty objective. Because \(v\) is selected in every original
minimum dominating set, each branch is evaluated under the selected-parent
quantity

\[
\min(A_i,B_i,C_i),
\]

whose minimizing state and count are branch-dependent. The
\(\gamma\)-excellent stable-root theorem therefore does not transfer.

The only burned exact strong-banked extremizer through order 14 remains
\(P_3\). TF22 does not promote that finite observation to an all-order
classification.

## 14. PPV audit

Petr--Portier--Versteegen's terminal transformations were reconsidered only
after the \(\gamma\)-excellent restriction was identified.

The restriction does not turn their fixed-\(\gamma\),
strong-support-sensitive inductive comparisons into an absolute
fixed-order inequality for either \(\zeta(T)\) or the hub pair
\((\zeta,\alpha)\). Their functional still changes with domination number
and strong-support bookkeeping. Thus TF22 does not import their terminal
grammar into the exact-order problem.

## 15. Burned diagnostics after theorem definitions

Only after the theorems above were fixed did TF22 inspect orders 1--14.

The deterministic reproducer is

`experiments/tf22_unique_empty_hub_diagnosis.py`.

It refuses every exhaustive order above 14. It checks:

- the critical-root \(C=\gamma-1\) equivalence on every burned all-flexible
  tree;
- stable attachment roots in every burned unique-empty tree;
- the \(W_{a,b}\) formulas whenever the named component itself lies in the
  burned range;
- the \(P_{3m+1}\) formulas for \(m\le4\);
- the smallest \(W_{2,2}\) versus \(W_{1,3}\) context reversal by combining
  already-computed component signatures algebraically;
- the burned all-flexible census and exact rooted-pair diversity;
- the burned unique-empty and strong-banked extremizer observations.

The diagnosis never constructs the larger full hub implied by the
\(P_7\)-context formula; it combines component signatures only. No order-15
or larger tree is generated.

The finite observations remain finite evidence. In particular:

- \(P_5\) is the only burned unique-empty exact extremizer;
- \(P_3\) is the only burned strong-banked exact extremizer.

Neither is promoted to an all-order threshold theorem.

## 16. Global grammars considered

**Gamma-excellent construction grammar.** Accepted as an exact shape
classification of the deletion components. Insufficient as an extremal
recurrence because rooted counts remain unbounded and context-sensitive.

**Stable-root rerooting.** Exact local optimum condition proved: minimize
\(\beta\) over stable roots. Insufficient because it does not classify the
stable optimum and critical rerooting can be harmful.

**Critical-root rewiring.** Rejected as monotone by the
\(P_{3m+1}\)+\(P_2\) analytic family.

**Equal-order component dominance.** Exact universal preorder identified as
coordinatewise dominance in \((\zeta,\alpha)\). It is genuinely
two-dimensional; no scalar compression is valid in all hub contexts.

**Cross-component exchange.** Exact aggregate preorder identified in
\((S,Q)\). It inherits the same two-dimensional obstruction.

**Balanced \(W\)-replacement.** Valid against the subdivided-star whole
tree, but not context-universal. \(W_{q,q}\) versus \(W_{q-1,q+1}\)
reverses according to the external flexible component.

**No-empty S-decomposition.** Still useful only after no-empty is known.
TF22 does not eliminate unique-empty hubs.

**Strong-banked normal form.** Remains sharply restricted by TF20 but not
excluded above \(P_3\).

No rejected route is replaced by additional burned-data mining.

## 17. Literature audit

The relevant structural sources are:

- T. Burton and D. P. Sumner,
  “\(\gamma\)-Excellent, critically dominated, end-dominated, and
  dot-critical trees are equivalent,”
  *Discrete Mathematics* 307 (2007), 683--693,
  DOI `10.1016/j.disc.2006.02.016`.
- V. Samodivkin,
  “Changing and unchanging of the domination number of a graph,”
  *Discrete Mathematics* 308 (2008), 5015--5025,
  DOI `10.1016/j.disc.2007.08.088`.
- V. Samodivkin,
  “Excellent graphs with respect to domination: subgraphs induced by minimum
  dominating sets,”
  *Discrete Mathematics Letters* 5 (2021), 12--19,
  DOI `10.47443/dml.2020.0052`.
- C. M. Mynhardt,
  “Vertices contained in every minimum dominating set of a tree,”
  *Journal of Graph Theory* 31 (1999), 163--177.
- D. S. Taletskii,
  “On the Number of Minimum Dominating Sets in Trees,”
  *Mathematical Notes* 113 (2023), 552--566.
- J. Petr, J. Portier and L. Versteegen,
  “On the number of minimum dominating sets and total dominating sets in
  forests,” *Journal of Graph Theory* 106 (2024), 976--993.

The audit distinguishes \(\gamma\)-excellent (“every vertex occurs in some
\(\gamma\)-set”) from TreeForge's initially stronger-looking all-flexible
condition. For nontrivial trees the extra no-universal condition follows
from the structural theorems above, but this equivalence is special to the
tree setting and the small exceptions must be retained.

A negative search for an exact unrestricted \(M_n\) theorem is not used as
novelty evidence.

## 18. Programme decision

TF22 reaches a mixed structural/negative endpoint.

What is now complete:

- the unique-empty no-universal class has an exact recursive shape
  characterization;
- its attachment roots are exactly stable vertices of nontrivial
  \(\gamma\)-excellent components;
- rerooting is fully accounted for;
- context-universal equal-order component dominance is characterized;
- context-universal two-component exchange is characterized;
- the natural \(W\)-balancing and critical-rerooting closure attempts have
  analytic counterfamilies.

What is not complete:

- no theorem reduces all stable-root \((\zeta,\alpha)\) pairs to a finite
  extremal menu;
- no theorem globally excludes unique-empty extremizers above \(P_5\);
- the no-empty S-decomposition side still lacks a complete exact-order
  extremal recurrence;
- the residual strong-banked class is not excluded above \(P_3\).

Therefore TF22 does **not** satisfy the prospective experiment-freeze
requirements.

- prospective \(M_{15}\): **not derived**;
- prospective order-15 extremizer family: **not derived**;
- order 15 consumed: **no**;
- new scientific experiment frozen: **no**;
- candidate allocated: **no**;
- candidate registry changed: **no**;
- experiment registry changed: **no**;
- next candidate ID: **TF-001158**;
- default invariant changed: **no**;
- `minimum_dominating_set_count` remains non-default theorem/diagnostic
  machinery.

The unrestricted multiplicity programme is therefore **paused**. TF22
identifies the unique-empty hub not as an unstructured residue, but as a
well-characterized \(\gamma\)-excellent stable-root construction whose exact
multiplicity optimization remains irreducibly context-sensitive under all
replacement mechanisms presently justified.

## 19. Recommended next session

Do not inspect order 15.

Do not continue the TF17--TF22 replacement line merely by enlarging the
burned census or refining local states. A continuation is justified only if
it starts from a genuinely new theorem-level input, such as:

- a published or independently proved extremal theorem for the stable-root
  \((\zeta,\alpha)\) Pareto envelope of \(\gamma\)-excellent trees;
- a context-aware global optimization theorem that handles the
  \(W_{a,b}\) antichain rather than trying to rank its members locally; or
- an all-order exclusion of the residual strong-banked class.

Absent such input, return TreeForge to question-audit mode and select a new
independent tree-theoretic question while preserving this programme as a
documented negative/structural result.
