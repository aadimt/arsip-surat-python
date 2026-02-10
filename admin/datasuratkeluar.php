<!DOCTYPE html>
<?php
session_start();
include "login/ceksession.php";
?>
<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <!-- Meta, title, CSS, favicons, etc. -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Arsip Surat Kantor Kecamatan Ciparay </title>

    <!-- Bootstrap -->
    <link href="../assets/vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="../assets/vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
    <!-- NProgress -->
    <link href="../assets/vendors/nprogress/nprogress.css" rel="stylesheet">
    <!-- iCheck -->
    <link href="../assets/vendors/iCheck/skins/flat/green.css" rel="stylesheet">
    <!-- Datatables -->
    <link href="../assets/vendors/datatables.net-bs/css/dataTables.bootstrap.min.css" rel="stylesheet">
    <link href="../assets/vendors/datatables.net-buttons-bs/css/buttons.bootstrap.min.css" rel="stylesheet">
    <link href="../assets/vendors/datatables.net-fixedheader-bs/css/fixedHeader.bootstrap.min.css" rel="stylesheet">
    <link href="../assets/vendors/datatables.net-responsive-bs/css/responsive.bootstrap.min.css" rel="stylesheet">
    <link href="../assets/vendors/datatables.net-scroller-bs/css/scroller.bootstrap.min.css" rel="stylesheet">
      <link rel="shortcut icon" href="../img/icon.ico">
    <!-- Custom Theme Style -->
    <link href="../assets/build/css/custom.min.css" rel="stylesheet">
  </head>

  <body class="nav-md">
    <div class="container body">
      <div class="main_container">
        <!-- Profile and Sidebarmenu -->
        <?php
        include("sidebarmenu.php");
        ?>
        <!-- /Profile and Sidebarmenu -->
        
        <!-- top navigation -->
        <?php
        include("header.php");
        ?>
        <!-- /top navigation -->

        <!-- page content -->
        <div class="right_col" role="main">
          <div class="">
            <div class="page-title">
              <div class="title_right">
                <h2>Surat Keluar ><small> Data Surat Keluar</small></h2>
              </div>
            </div>

            <div class="clearfix"></div>

            <div class="row">
              <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="x_panel">
                  <div class="x_title">
                    <h2>Data<small>Surat Keluar</small></h2>
                    <div class="clearfix"></div>
                  </div>
                   <form method="get" id="filterForm" class="form-horizontal form-label-left">
                        <div class="col-md-2 col-sm-2 col-xs-6">
                          <select name="bulan" class="form-control" onchange="document.getElementById('filterForm').submit()">
                            <option value="">Pilih Bulan</option>
                            <option value="01" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="01") echo 'selected'; ?>>Januari</option>
                            <option value="02" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="02") echo 'selected'; ?>>Februari</option>
                            <option value="03" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="03") echo 'selected'; ?>>Maret</option>
                            <option value="04" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="04") echo 'selected'; ?>>April</option>
                            <option value="05" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="05") echo 'selected'; ?>>Mei</option>
                            <option value="06" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="06") echo 'selected'; ?>>Juni</option>
                            <option value="07" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="07") echo 'selected'; ?>>Juli</option>
                            <option value="08" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="08") echo 'selected'; ?>>Agustus</option>
                            <option value="09" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="09") echo 'selected'; ?>>September</option>
                            <option value="10" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="10") echo 'selected'; ?>>Oktober</option>
                            <option value="11" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="11") echo 'selected'; ?>>November</option>
                            <option value="12" <?php if(isset($_GET['bulan']) && $_GET['bulan']=="12") echo 'selected'; ?>>Desember</option>
                          </select>
                        </div>
                        <div class="col-md-2 col-sm-2 col-xs-6">
                          <select name="tahun" class="form-control" onchange="document.getElementById('filterForm').submit()">
                            <option value="">Pilih Tahun</option>
                            <?php
                                for ($th=2005;$th<=2040;$th++)
                                      {
                                       $sel = (isset($_GET['tahun']) && $_GET['tahun']==$th) ? ' selected' : '';
                                       echo  '<option value="'.$th.'"'.$sel.'>'.$th.'</option>';
                                      }
                            ?>
                          </select>
                        </div>
                  <?php
                    $bparam = isset($_GET['bulan']) ? $_GET['bulan'] : '';
                    $yparam = isset($_GET['tahun']) ? $_GET['tahun'] : '';
                    $downloadHref = 'downloadlaporan_suratkeluar.php';
                    if ($bparam!=='' || $yparam!=='') {
                        $downloadHref .= '?';
                        $pairs = array();
                        if ($bparam!=='') $pairs[] = 'bulan=' . urlencode($bparam);
                        if ($yparam!=='') $pairs[] = 'tahun=' . urlencode($yparam);
                        $downloadHref .= implode('&', $pairs);
                    }
                  ?>
                  <a href="<?php echo $downloadHref;?>" class="btn btn-success"><i class="fa fa-download"></i> Unduh Laporan Surat Keluar</a>
                  <a href="inputsuratkeluar.php"><button type="button" class="btn btn-success"><i class="fa fa-plus"></i> Tambah Surat Keluar</button></a>
                  </form>
                  <div class="x_content">
                  <div class="x_content">
                              <?php
                              include '../koneksi/koneksi.php';

                              $bulan = isset($_GET['bulan']) ? trim($_GET['bulan']) : '';
                              $tahun = isset($_GET['tahun']) ? trim($_GET['tahun']) : '';

                              $where = [];
                              if ($bulan !== '') {
                                  $b = intval($bulan);
                                  $where[] = "MONTH(tanggalkeluar_suratkeluar) = $b";
                              }
                              if ($tahun !== '') {
                                  $y = intval($tahun);
                                  $where[] = "YEAR(tanggalkeluar_suratkeluar) = $y";
                              }

                              $filter = '';
                              if (!empty($where)) {
                                  $filter = 'WHERE ' . implode(' AND ', $where);
                              }

                              $sql1		= "SELECT * FROM tb_suratkeluar $filter order by id_suratkeluar asc";
                              $query1  	= mysqli_query($db, $sql1);
                              $total		= mysqli_num_rows($query1);
                              if ($total == 0) {
                                echo"<center><h2>Belum Ada Data Surat Keluar</h2></center>";
                              }
                              else{?>
                    <table id="datatable" class="table table-striped table-bordered">
                      <thead>
                        <tr>
                          <th width="15%">Nomor Surat</th>
                          <th width="10%">Tanggal Keluar</th>
                          <th width="5%">Kode Surat</th>
                          <th width="10%">Tanggal Surat</th>
                          <th width="10%">Bagian</th>
                          <th width="15%">Kepada</th>
                          <th width="21%">Perihal</th>
                          <th width="14%">Aksi</th>
                        </tr>
                      </thead>


                      <tbody>
                            <?php
                            while($data = mysqli_fetch_array($query1)){
                              echo'<tr>
                              <td>	'. $data['nomor_suratkeluar'].'  	</td>
                              <td>	'. $data['tanggalkeluar_suratkeluar'].'		</td>
                              <td>	'. $data['kode_suratkeluar'].'	</td>
                              <td>	'. $data['tanggalsurat_suratkeluar'].'  		</td>
                              <td>	'. $data['nama_bagian'].'  		</td>
                              <td>	'. $data['kepada_suratkeluar'].'		</td>
                              <td>  '. $data['perihal_suratkeluar'].'  </td> 
                              <td style="text-align:center;">
                              <a href= surat_keluar/'.$data['file_suratkeluar'].'><button type="button" title="Unduh File" class="btn btn-success btn-xs"><i class="fa fa-download"></i></button></a>
                              <a href=detail-suratkeluar.php?id_suratkeluar='.$data['id_suratkeluar'].'><button type="button" title="Detail" class="btn btn-info btn-xs"><i class="fa fa-file-image-o"></i></button></a>
                              <a href=editsuratkeluar.php?id_suratkeluar='.$data['id_suratkeluar'].'><button type="button" title="Edit" class="btn btn-default btn-xs"><i class="fa fa-edit"></i></button></a>
                              <a onclick="return konfirmasi()" href=proses/proses_hapussuratkeluar.php?id_suratkeluar='.$data['id_suratkeluar'].'><button type="button" title="Hapus" class="btn btn-danger btn-xs"><i class="fa fa-trash-o"></i></button></a></td>
                              </tr>';
                            }
                            ?>
                      </tbody>
                    </table>
                    <?php } ?>
                  </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- /page content -->

        <!-- footer content -->
        <footer>
          <div class="pull-right">
          </div>
          <div class="clearfix"></div>
        </footer>
        <!-- /footer content -->
      </div>
    </div>

    <!-- jQuery -->
    <script src="../assets/vendors/jquery/dist/jquery.min.js"></script>
    <!-- Bootstrap -->
    <script src="../assets/vendors/bootstrap/dist/js/bootstrap.min.js"></script>
    <!-- FastClick -->
    <script src="../assets/vendors/fastclick/lib/fastclick.js"></script>
    <!-- NProgress -->
    <script src="../assets/vendors/nprogress/nprogress.js"></script>
    <!-- iCheck -->
    <script src="../assets/vendors/iCheck/icheck.min.js"></script>
    <!-- Datatables -->
    <script src="../assets/vendors/datatables.net/js/jquery.dataTables.min.js"></script>
    <script src="../assets/vendors/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>
    <script src="../assets/vendors/datatables.net-buttons/js/dataTables.buttons.min.js"></script>
    <script src="../assets/vendors/datatables.net-buttons-bs/js/buttons.bootstrap.min.js"></script>
    <script src="../assets/vendors/datatables.net-buttons/js/buttons.flash.min.js"></script>
    <script src="../assets/vendors/datatables.net-buttons/js/buttons.html5.min.js"></script>
    <script src="../assets/vendors/datatables.net-buttons/js/buttons.print.min.js"></script>
    <script src="../assets/vendors/datatables.net-fixedheader/js/dataTables.fixedHeader.min.js"></script>
    <script src="../assets/vendors/datatables.net-keytable/js/dataTables.keyTable.min.js"></script>
    <script src="../assets/vendors/datatables.net-responsive/js/dataTables.responsive.min.js"></script>
    <script src="../assets/vendors/datatables.net-responsive-bs/js/responsive.bootstrap.js"></script>
    <script src="../assets/vendors/datatables.net-scroller/js/dataTables.scroller.min.js"></script>
    <script src="../assets/vendors/jszip/dist/jszip.min.js"></script>
    <script src="../assets/vendors/pdfmake/build/pdfmake.min.js"></script>
    <script src="../assets/vendors/pdfmake/build/vfs_fonts.js"></script>

    <!-- Custom Theme Scripts -->
    <script src="../assets/build/js/custom.min.js"></script>
    <style>
    .highlight-term { background-color: #fff176; padding: 0 3px; border-radius: 2px; }
    </style>
    <script>
    (function($){
      function escapeRegExp(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
      function applyHighlights(table, term){
        var $tbody = $(table.table().body());
        $tbody.find('span.highlight-term').each(function(){ $(this).replaceWith($(this).text()); });
        if (!term) return;
        var regex = new RegExp('(' + escapeRegExp(term) + ')', 'gi');
        $tbody.find('td').each(function(){
          var $td = $(this);
          // skip action column (contains buttons)
          if ($td.find('a,button').length && $td.text().trim().length < 1) return;
          var html = $td.html();
          var newHtml = html.replace(regex, '<span class="highlight-term">$1</span>');
          if (newHtml !== html) $td.html(newHtml);
        });
      }
      $(document).ready(function(){
        if ($.fn.DataTable){
          var table = $('#datatable').DataTable();
          // apply currently present search (if any)
          applyHighlights(table, table.search());
          table.on('search.dt draw.dt', function(){ applyHighlights(table, table.search()); });
        }
      });
    })(jQuery);
    </script>
    <script type="text/javascript" language="JavaScript">
        function konfirmasi()
        {
        tanya = confirm("Anda Yakin Akan Menghapus Data ?");
        if (tanya == true) return true;
        else return false;
        }
    </script>

  </body>
</html>